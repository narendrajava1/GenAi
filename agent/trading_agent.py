# agent/trading_agent.py

import json
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_core.tools import FunctionTool

from tools.trade_tools import trade_calculator, multi_target_calculator, target_calculator

# ── Ollama Client ─────────────────────────────────────────────────────────────

ollama_client = OllamaChatCompletionClient(
    model="llama3.1",
    host="http://localhost:11434",
    model_capabilities={
        "vision": False,
        "function_calling": True,
        "json_output": True,
    },
)

# ── Register Tools ────────────────────────────────────────────────────────────

trade_tool       = FunctionTool(trade_calculator,       description="Calculate profit/loss/charges for a single target options trade.")
multi_trade_tool = FunctionTool(multi_target_calculator, description="Calculate trade details for multiple targets e.g. TARGET: 600 / 700.")
target_tool      = FunctionTool(target_calculator,       description="Calculate suggested target price based on risk-reward ratio.")

# ── System Prompt ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are an expert Indian options trading assistant.

You have THREE tools:

┌──────────────────────────────────────────────────────────────────┐
│ TOOL 1: trade_calculator                                         │
│   Use for: single target price                                   │
│   Params : symbol, lots, buy_price, sell_price, stop_loss        │
│                                                                  │
│ TOOL 2: multi_target_calculator                                  │
│   Use for: multiple targets e.g. "TARGET: 600 / 700"            │
│   Params : symbol, lots, buy_price, targets (list), stop_loss    │
│                                                                  │
│ TOOL 3: target_calculator                                        │
│   Use for: suggested target from R:R ratio                       │
│   Params : buy_price, sl, rr (default 1.5)                       │
└──────────────────────────────────────────────────────────────────┘

SYMBOL EXTRACTION RULES:
  Strip: BUY, SELL, SHORT, LONG, ABOVE, BELOW, AT
  "BUY NIFTY 22350 PE ABOVE" → symbol = "NIFTY 22350 PE"
  "ABOVE 550"  → buy_price = 550
  "SL :- 460"  → stop_loss = 460
  "TARGET :- 600 / 700" → targets = [600, 700]
  Valid indices: NIFTY, BANKNIFTY, FINNIFTY, MIDCPNIFTY, SENSEX

CASE 1 — SINGLE TARGET:
  Call 1 → trade_calculator(symbol, lots, buy_price, sell_price, stop_loss)
  Call 2 → target_calculator(buy_price, sl=stop_loss, rr=1.5)
  Call 3 → trade_calculator(symbol, lots, buy_price, sell_price=<Call2 result>, stop_loss)

CASE 2 — MULTIPLE TARGETS:
  Call 1 → multi_target_calculator(symbol, lots, buy_price, targets=[t1,t2], stop_loss)
  Call 2 → target_calculator(buy_price, sl=stop_loss, rr=1.5)

After all tool calls, respond with a JSON object ONLY (no extra text):

For CASE 1:
{
  "symbol": "NIFTY 18000 CE",
  "lots": 2,
  "qty": 150,
  "orders": [150],
  "investment": 18000.0,
  "buy_price": 120.0,
  "stop_loss": 100.0,
  "break_even": 18120.0,
  "charges": 68.08,
  "your_target": {
    "sell_price": 150.0,
    "net_profit": 4431.92,
    "profit_percent": 24.62,
    "risk_reward": 1.5,
    "loss_with_charges": 3068.08
  },
  "suggested_target": {
    "sell_price": 150.0,
    "net_profit": 4431.92,
    "profit_percent": 24.62,
    "risk_reward": 1.5,
    "loss_with_charges": 3068.08
  },
  "insight": "Good R:R — risk is well controlled."
}

For CASE 2 (multiple targets):
{
  "symbol": "SENSEX 71900 PE",
  "lots": 100,
  "qty": 1000,
  "orders": [1000],
  "investment": 550000.0,
  "buy_price": 550.0,
  "stop_loss": 460.0,
  "break_even": 71350.0,
  "charges": 1234.0,
  "loss_at_stoploss": 90000.0,
  "loss_with_charges": 91234.0,
  "targets": [
    {"target": 600, "net_profit": 49120.0, "profit_percent": 8.93, "risk_reward": 0.5, "charges": 1234.0},
    {"target": 700, "net_profit": 148880.0, "profit_percent": 27.07, "risk_reward": 1.6, "charges": 1234.0}
  ],
  "suggested_price": 685.0,
  "insight": "T2 at ₹700 offers strong R:R — hold if trend is bullish."
}

ERROR HANDLING:
  If any tool returns {"error": "..."}, respond with:
  {"error": "<message>", "fix": "<what user should correct>"}
  Then say TERMINATE.

Always end your final message with: TERMINATE
"""

# ── Agent ─────────────────────────────────────────────────────────────────────

trading_agent = AssistantAgent(
    name="TradingAgent",
    model_client=ollama_client,
    tools=[trade_tool, multi_trade_tool, target_tool],
    system_message=SYSTEM_PROMPT,
    reflect_on_tool_use=True,
)

termination  = TextMentionTermination("TERMINATE")
trading_team = RoundRobinGroupChat(
    participants=[trading_agent],
    termination_condition=termination,
    max_turns=10,
)

# ── Public API ────────────────────────────────────────────────────────────────

async def ask_agent(user_input: str) -> dict:
    """
    Run the trading agent and return a structured dict.

    Returns:
        dict — always contains at least one of:
            - trade fields (symbol, lots, qty, ...) on success
            - {"error": "...", "fix": "..."} on tool error
            - {"raw": "..."} if JSON parsing fails
    """
    result = await trading_team.run(task=user_input)

    # Collect the last assistant text message
    last_text = ""
    for msg in reversed(result.messages):
        if hasattr(msg, "content") and isinstance(msg.content, str) and msg.content.strip():
            last_text = msg.content.replace("TERMINATE", "").strip()
            break

    # ── Try to parse JSON from the agent's response ───────────────────────
    try:
        # Agent might wrap JSON in markdown code block — strip it
        clean = last_text
        if "```json" in clean:
            clean = clean.split("```json")[1].split("```")[0].strip()
        elif "```" in clean:
            clean = clean.split("```")[1].split("```")[0].strip()

        return json.loads(clean)

    except (json.JSONDecodeError, IndexError):
        # Return raw text if JSON parsing fails — app.py handles this gracefully
        return {"raw": last_text}