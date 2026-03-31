# api/app.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import Optional
from agent.trading_agent import ask_agent

# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Trading AI Agent",
    description="Options trading assistant powered by AutoGen + Ollama",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Schemas ───────────────────────────────────────────────────────────────────

class TradeRequest(BaseModel):
    query: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"query": "Buy NIFTY 18000 CE 2 lots at 120 sell at 150 stoploss 100"},
                {"query": "BUY SENSEX 71900 PE ABOVE 550 TARGET :- 600 / 700 SL :- 460 lots 100"},
                {"query": "What is my target if I buy at 200 and SL is 160?"},
            ]
        }
    }


class TargetBreakdown(BaseModel):
    label: str
    target_price: float
    net_pnl: float
    profit_percent: float
    risk_reward: str
    loss_at_sl: float


class TradeSummary(BaseModel):
    symbol: str
    quantity: int
    lots: int
    orders: int
    investment: float
    buy_price: float
    stop_loss: float
    break_even: float
    charges: float
    targets: list[TargetBreakdown]
    insight: str


class TradeResponse(BaseModel):
    query: str
    status: str                         # "success" | "error" | "info"
    summary: Optional[TradeSummary]     # structured JSON for UI rendering
    message: str                        # formatted text for display / terminal


# ── Formatter ─────────────────────────────────────────────────────────────────

def _inr(value: float) -> str:
    return f"₹{value:,.2f}"


def build_formatted_message(summary: TradeSummary) -> str:
    DIV  = "━" * 54
    THIN = "─" * 54
    lines = []

    lines += [
        DIV,
        f"  📋 TRADE SUMMARY  ·  {summary.symbol}",
        DIV,
        f"  📦 Quantity    : {summary.quantity} units  |  {summary.lots} lots  |  {summary.orders} order(s)",
        f"  💰 Investment  : {_inr(summary.investment)}",
        f"  🛒 Buy Price   : {_inr(summary.buy_price)}",
        f"  🔴 Stop Loss   : {_inr(summary.stop_loss)}",
        f"  ⚖️  Break-Even  : {_inr(summary.break_even)}",
        f"  🧾 Charges     : {_inr(summary.charges)}",
        "",
    ]

    if len(summary.targets) == 1:
        t = summary.targets[0]
        lines += [
            THIN,
            f"  🎯 Target      : {_inr(t.target_price)}",
            f"  ✅ Net P&L     : {_inr(t.net_pnl)}  ({t.profit_percent:.2f}%)",
            f"  📊 Risk-Reward : {t.risk_reward}",
            f"  ❌ Loss @ SL   : {_inr(t.loss_at_sl)}",
        ]

    elif len(summary.targets) == 2:
        t1, t2 = summary.targets[0], summary.targets[1]
        W = 20

        def row(label: str, v1: str, v2: str) -> str:
            return f"  {label:<14}  {v1:<{W}}  {v2:<{W}}"

        lines += [
            THIN,
            f"  {'':14}  {t1.label:<{W}}  {t2.label:<{W}}",
            THIN,
            row("🎯 Target",  _inr(t1.target_price),       _inr(t2.target_price)),
            row("✅ Net P&L", _inr(t1.net_pnl),            _inr(t2.net_pnl)),
            row("📈 Profit%", f"{t1.profit_percent:.2f}%", f"{t2.profit_percent:.2f}%"),
            row("📊 R:R",     t1.risk_reward,               t2.risk_reward),
            row("❌ Loss@SL", _inr(t1.loss_at_sl),          _inr(t2.loss_at_sl)),
        ]

    else:
        lines.append(THIN)
        for t in summary.targets:
            lines += [
                f"  🎯 {t.label}  :  {_inr(t.target_price)}",
                f"     ✅ Net P&L   : {_inr(t.net_pnl)}  ({t.profit_percent:.2f}%)",
                f"     📊 R:R       : {t.risk_reward}",
                f"     ❌ Loss @ SL : {_inr(t.loss_at_sl)}",
                "",
            ]

    lines += [DIV, f"  💬 {summary.insight}"]
    return "\n".join(lines)


# ── Summary Builder ───────────────────────────────────────────────────────────

def build_summary(data: dict) -> tuple[Optional[TradeSummary], str]:
    """
    Parse the structured dict returned by ask_agent() into
    a TradeSummary + formatted message string.

    Returns (None, error_message) if data contains an error or raw fallback.
    """

    # ── Error from tool ───────────────────────────────────────────────────
    if "error" in data:
        msg = f"⚠️  {data['error']}"
        if "fix" in data:
            msg += f"\n💡 Fix: {data['fix']}"
        return None, msg

    # ── Raw fallback (JSON parse failed) ──────────────────────────────────
    if "raw" in data:
        return None, data["raw"]

    # ── Build targets list ────────────────────────────────────────────────
    targets: list[TargetBreakdown] = []

    # Case 1: single target with your_target + suggested_target
    if "your_target" in data:
        yt = data["your_target"]
        targets.append(TargetBreakdown(
            label="Your Target",
            target_price=yt.get("sell_price", 0),
            net_pnl=yt.get("net_profit", 0),
            profit_percent=yt.get("profit_percent", 0),
            risk_reward=f"1:{yt.get('risk_reward', 0)}",
            loss_at_sl=yt.get("loss_with_charges", 0),
        ))

    if "suggested_target" in data:
        sg = data["suggested_target"]
        targets.append(TargetBreakdown(
            label="Suggested Target",
            target_price=sg.get("sell_price", 0),
            net_pnl=sg.get("net_profit", 0),
            profit_percent=sg.get("profit_percent", 0),
            risk_reward=f"1:{sg.get('risk_reward', 0)}",
            loss_at_sl=sg.get("loss_with_charges", 0),
        ))

    # Case 2: multi-target list
    if "targets" in data:
        targets = []
        loss_sl = data.get("loss_with_charges", 0)
        for t in data["targets"]:
            targets.append(TargetBreakdown(
                label=f"Target ₹{t['target']}",
                target_price=t["target"],
                net_pnl=t.get("net_profit", 0),
                profit_percent=t.get("profit_percent", 0),
                risk_reward=f"1:{t.get('risk_reward', 0)}",
                loss_at_sl=loss_sl,
            ))

    summary = TradeSummary(
        symbol=data.get("symbol", ""),
        quantity=data.get("qty", 0),
        lots=data.get("lots", 0),
        orders=len(data.get("orders", [1])),
        investment=data.get("investment", 0),
        buy_price=data.get("buy_price", 0),
        stop_loss=data.get("stop_loss", 0),
        break_even=data.get("break_even", 0),
        charges=data.get("charges", 0),
        targets=targets,
        insight=data.get("insight", ""),
    )

    return summary, build_formatted_message(summary)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "service": "Trading AI Agent",
        "powered_by": "AutoGen 0.4 + Ollama (llama3.1)",
        "endpoints": {
            "POST /trade":      "Submit a trade query (JSON response)",
            "POST /trade/text": "Submit a trade query (plain text response)",
            "GET  /health":     "Health check",
            "GET  /docs":       "Swagger UI",
        },
    }


@app.get("/health")
async def health():
    return {"status": "ok", "agent": "TradingAgent", "model": "llama3.1"}


@app.post("/trade", response_model=TradeResponse)
async def trade(request: TradeRequest):
    """
    Submit a trade query. Returns structured JSON + formatted text message.

    - `summary` : structured data for frontend/UI rendering
    - `message` : formatted text for terminal / chat / Telegram display
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        data = await ask_agent(request.query)           # always returns dict now
        print("DEBUG: Raw agent output:", data)          # log raw output for debugging
        summary, message = build_summary(data)

        return TradeResponse(
            query=request.query,
            status="error" if "error" in data else "success",
            summary=summary,
            message=message,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/trade/text", response_class=PlainTextResponse)
async def trade_text(request: TradeRequest) -> str:
    """
    Returns the trade summary as plain text.
    Preserves exact formatting, newlines, and emoji alignment.
    Ideal for terminal display, Telegram bots, or WhatsApp.
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    data = await ask_agent(request.query)
    _, message = build_summary(data)
    return message