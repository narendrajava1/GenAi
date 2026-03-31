# 🤖 Options Trading AI Agent

> **Agentic AI system for Indian options trading** — powered by local LLMs via Ollama, with two implementations: **LangChain** and **Microsoft AutoGen**.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-green?style=flat-square)](https://langchain.com)
[![AutoGen](https://img.shields.io/badge/AutoGen-0.4+-purple?style=flat-square)](https://microsoft.github.io/autogen)
[![Ollama](https://img.shields.io/badge/Ollama-llama3.1-orange?style=flat-square)](https://ollama.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-teal?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

---

## 📌 Overview

This project demonstrates **real-world agentic AI** applied to Indian options trading. Instead of hardcoded logic, an LLM acts as the reasoning brain — autonomously deciding which tools to call, in what order, and how to chain results across multiple steps.

The agent understands **natural language trade queries**, extracts structured parameters, calls domain-specific financial tools, and returns a complete trade analysis — all running **100% locally with zero API costs**.

### Why Agentic? Why Not Just a Calculator?

| Approach | Capability |
|---|---|
| Plain calculator | Fixed inputs → fixed output |
| LLM only | Can explain trades, can't compute |
| LLM + hardcoded API | Can call one tool, no decision-making |
| **AI Agent (this project)** | Decides which tools to call, chains results, handles edge cases, understands natural language |

---

## ✨ Features

- 🧠 **Agentic reasoning** — LLM decides tool call order dynamically
- 💬 **Natural language input** — no strict format required
- 🎯 **Single & multi-target support** — `TARGET: 600 / 700` parsed automatically
- 💡 **Suggested target** — auto-calculated at 1:1.5 R:R via `target_calculator`
- 📊 **Side-by-side comparison** — your target vs suggested target
- 💰 **Full trade breakdown** — gross profit, net profit, charges, break-even, risk-reward, loss at SL
- 🔣 **Symbol sanitization** — strips BUY/SELL/ABOVE from input automatically
- 🔁 **Two implementations** — LangChain (CLI) + AutoGen (FastAPI REST API)
- 🏠 **100% local** — Ollama, no OpenAI, no cloud API costs

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Input                           │
│   "BUY NIFTY 22350 PE ABOVE 35 TARGET 55 SL 9 2 lots"      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   Ollama LLM (llama3.1)                     │
│              [ Reasoning & Tool Selection ]                 │
└──────┬──────────────┬───────────────────────────┬──────────┘
       │              │                           │
       ▼              ▼                           ▼
┌──────────┐  ┌───────────────┐  ┌───────────────────────┐
│  trade_  │  │    target_    │  │   multi_target_       │
│calculator│  │   calculator  │  │      calculator       │
└──────┬───┘  └───────┬───────┘  └───────────┬───────────┘
       │              │                       │
       └──────────────┼───────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Trade Service Layer                        │
│              services/trade_service.py                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    Trade Model                              │
│   models/trade.py  — lot size, order splitting, charges     │
└─────────────────────────────────────────────────────────────┘
```

### Agent Tool Call Flow (Single Target)

```
Call 1 → trade_calculator(symbol, lots, buy_price, sell_price, stop_loss)
              ↓ returns: net_profit, charges, risk_reward, break_even ...
Call 2 → target_calculator(buy_price, sl=stop_loss, rr=1.5)
              ↓ returns: suggested_target
Call 3 → trade_calculator(symbol, lots, buy_price, sell_price=suggested_target, stop_loss)
              ↓ returns: profit at suggested target
              ↓
    Side-by-side comparison rendered
```

---

## 📁 Project Structure

```
GenAi/
├── langchain-trading/              # LangChain implementation (CLI)
│   ├── config/
│   │   └── broker_config.py        # Lot sizes & max qty per index
│   ├── models/
│   │   └── trade.py                # Core Trade model & calculations
│   ├── services/
│   │   └── trade_service.py        # Service layer
│   ├── tools/
│   │   └── trade_tools.py          # LangChain @tool definitions
│   ├── agent/
│   │   └── trading_agent.py        # Agent setup, prompt, memory
│   ├── main.py                     # CLI entry point
│   └── requirements.txt
│
└── autogen-trading/                # AutoGen implementation (FastAPI)
    ├── config/
    │   └── broker_config.py
    ├── models/
    │   └── trade.py
    ├── services/
    │   └── trade_service.py
    ├── tools/
    │   └── trade_tools.py          # Plain Python functions (FunctionTool)
    ├── agent/
    │   └── trading_agent.py        # AutoGen AssistantAgent + team
    ├── api/
    │   └── app.py                  # FastAPI REST endpoints
    ├── main.py                     # Uvicorn entry point
    └── requirements.txt
```

---

## ⚙️ Supported Indices

| Index | Lot Size | Max Qty/Order |
|---|---|---|
| NIFTY | 75 | 1800 |
| BANKNIFTY | 15 | 900 |
| FINNIFTY | 40 | 1800 |
| MIDCPNIFTY | 75 | 2100 |
| SENSEX | 10 | 1000 |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com) installed and running
- llama3.1 model pulled

```bash
# Install Ollama (macOS/Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Pull the model
ollama pull llama3.1

# Start Ollama server
ollama serve
```

> **Note:** `qwen2.5` or `mistral` can also be used. Update `model` in `agent/trading_agent.py`.

---

## 🦜 Option 1: LangChain (CLI)

```bash
cd langchain-trading

# Install dependencies
pip install -r requirements.txt

# Run interactive CLI
python main.py

# Or single query mode
python main.py "BUY NIFTY 22350 PE ABOVE 35, sell 55, SL 9, 2 lots"
```

**Example session:**
```
You: BUY SENSEX 71900 PE ABOVE 550 TARGET :- 600 / 700 SL :- 460 lots 100

Agent:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 TRADE SUMMARY  —  SENSEX 71900 PE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Quantity    : 1000 units  |  100 lots  |  1 order(s)
💰 Investment  : ₹5,50,000
🛒 Buy Price   : ₹550
🔴 Stop Loss   : ₹460

         T1: ₹600    T2: ₹700    💡 SUGGESTED
🎯 Target  ₹600      ₹700        ₹685
✅ Net P&L ₹49,120   ₹1,48,880   —
📈 Profit% 8.9%      27.07%      —
📊 R:R     1:0.5     1:1.6       1:1.5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 T2 at ₹700 offers a strong R:R — worth holding if trend is bullish.
```

---

## ⚡ Option 2: AutoGen + FastAPI (REST API)

```bash
cd autogen-trading

# Install dependencies
pip install -r requirements.txt

# Start the API server
python main.py
```

Server runs at: **http://localhost:8000**
Swagger docs at: **http://localhost:8000/docs**

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Service info |
| `GET` | `/health` | Health check |
| `POST` | `/trade` | Submit trade query |

### Request & Response

**POST `/trade`**

```json
// Request
{
  "query": "BUY NIFTY 22350 PE ABOVE 35, sell 55, SL 9, 2 lots"
}

// Response
{
  "query": "BUY NIFTY 22350 PE ABOVE 35, sell 55, SL 9, 2 lots",
  "response": "📋 TRADE SUMMARY — NIFTY 22350 PE\n...",
  "status": "success"
}
```

### cURL Examples

```bash
# Single target
curl -X POST http://localhost:8000/trade \
  -H "Content-Type: application/json" \
  -d '{"query": "BUY NIFTY 22350 PE ABOVE 35, sell 55, SL 9, 2 lots"}'

# Multiple targets
curl -X POST http://localhost:8000/trade \
  -H "Content-Type: application/json" \
  -d '{"query": "BUY SENSEX 71900 PE ABOVE 550 TARGET :- 600 / 700 SL :- 460 lots 100"}'

# Target price only
curl -X POST http://localhost:8000/trade \
  -H "Content-Type: application/json" \
  -d '{"query": "What is my target if I buy at 200 and SL is 160?"}'
```

---

## 💬 Example Queries

The agent understands **messy, natural language** — no strict format needed:

```bash
# Standard trade
"NIFTY 18000 CE, 2 lots, buy 200, sell 280, stop loss 160"

# With BUY/SELL prefix (auto-sanitized)
"BUY BANKNIFTY 44000 PE, 1 lot, entry 350, target 500, SL 280"

# ABOVE keyword (auto-parsed as buy_price)
"BUY NIFTY 22350 PE ABOVE 35 TARGET 55 SL 9 2 lots"

# Multiple targets
"BUY SENSEX 71900 PE ABOVE 550 TARGET :- 600 / 700 SL :- 460 lots 100"

# Target price only
"What is my target at 1:2 RR if I buy at 200 and SL is 160?"

# Conversational follow-up (LangChain only)
"Recalculate with 3 lots instead"
"What if I change RR to 2?"
```

---

## 🛠️ Tools

### `trade_calculator`
Calculates full trade breakdown for a **single target**.

| Parameter | Type | Description |
|---|---|---|
| `symbol` | `str` | `INDEX STRIKE CE/PE` — e.g. `NIFTY 18000 CE` |
| `lots` | `int` | Number of lots |
| `buy_price` | `float` | Entry premium |
| `sell_price` | `float` | Exit target premium |
| `stop_loss` | `float` | Stop loss premium |

**Returns:** `gross_profit`, `net_profit`, `charges`, `investment`, `profit_percent`, `break_even`, `risk_reward`, `loss_at_stoploss`, `loss_with_charges`

---

### `multi_target_calculator`
Calculates trade breakdown for **multiple targets** simultaneously.

| Parameter | Type | Description |
|---|---|---|
| `symbol` | `str` | `INDEX STRIKE CE/PE` |
| `lots` | `int` | Number of lots |
| `buy_price` | `float` | Entry premium |
| `targets` | `list[float]` | e.g. `[600, 700]` |
| `stop_loss` | `float` | Stop loss premium |

---

### `target_calculator`
Calculates **suggested target** from risk-reward ratio.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `buy_price` | `float` | — | Entry price |
| `sl` | `float` | — | Stop loss price |
| `rr` | `float` | `1.5` | Risk-reward ratio |

**Formula:** `target = buy_price + (buy_price - sl) × rr`

---

## 🔄 LangChain vs AutoGen — Comparison

| Feature | LangChain | AutoGen |
|---|---|---|
| **Version** | 0.2+ | 0.4+ |
| **Interface** | CLI | FastAPI REST |
| **Tool Definition** | `@tool` decorator | `FunctionTool` wrapper |
| **Agent Loop** | `AgentExecutor` | `RoundRobinGroupChat` team |
| **Memory** | `InMemoryChatMessageHistory` | Session via `max_turns` |
| **Termination** | `max_iterations` | `TextMentionTermination` |
| **Async** | Optional | Native `async/await` |
| **Multi-agent** | Manual | Built-in team support |
| **Best for** | Quick prototypes, CLI tools | Production APIs, multi-agent systems |

---

## 🧪 Charges Formula

Brokerage and exchange charges are calculated per order:

```
charges_per_order = 40 + (buy_price + sell_price) × qty × 0.0008
```

Orders are split automatically when `qty > max_qty` per exchange limits.

---

## 🗺️ Roadmap

- [ ] Live market price fetch via broker API (Zerodha/Upstox)
- [ ] Portfolio-level risk tracking
- [ ] WebSocket streaming responses
- [ ] Telegram / WhatsApp bot interface
- [ ] Multi-agent setup: Research Agent + Trade Agent + Risk Agent
- [ ] Support for futures (not just options)
- [ ] Backtesting tool integration

---

## 🤝 Contributing

Contributions are welcome! To add a new index:

1. Add to `config/broker_config.py`:
```python
"MIDCAP": {
    "lot_size": 50,
    "max_qty": 1500,
}
```
2. That's it — the Trade model and all tools pick it up automatically.

---

## ⚠️ Disclaimer

This project is for **educational and demonstration purposes only**. It is not financial advice. Always consult a SEBI-registered advisor before trading. Options trading involves significant risk of loss.

---

## 👨‍💻 Author

**Narendra Java**
- GitHub: [@narendrajava1](https://github.com/narendrajava1)
- Repository: [GenAi — feature/tool_agent](https://github.com/narendrajava1/GenAi/tree/feature/tool_agent)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
  <strong>⭐ Star this repo if it helped you understand AI Agents!</strong><br/>
  Built with ❤️ using Ollama + LangChain + AutoGen
</div>

Let me give you a thorough walkthrough of both files visually.Let me walk you through both files with clear diagrams and explanations.**`trading_agent.py`** is the brain — here is each section explained:

**`OllamaChatCompletionClient`** — this is the LLM connection. `function_calling: True` tells AutoGen that this model can decide when and how to invoke tools. `temperature=0` makes it deterministic — critical for financial numbers, you don't want the LLM being "creative" with rupee amounts.

**`FunctionTool`** — AutoGen 0.4 does not use LangChain's `@tool` decorator. Instead you wrap a plain Python function in `FunctionTool`. AutoGen reads the function's type hints and docstring and converts them into a JSON schema that gets sent to the LLM so it knows what parameters each tool expects.

**`AssistantAgent`** — the actual agent. It holds the LLM client, the list of tools, and the system prompt. `reflect_on_tool_use=True` is important — it means after each tool call, the agent re-reads the result before deciding whether to call another tool or respond. Without this, it would call tools and immediately respond without incorporating results.

**`RoundRobinGroupChat`** — this is AutoGen's agent loop orchestrator. Even with one agent it is required to run the conversation. `max_turns=10` prevents infinite loops. `TextMentionTermination("TERMINATE")` stops the loop the moment the agent outputs that word.

**`ask_agent()`** — this is the public function `app.py` calls. It runs the team, finds the last assistant message, strips the `TERMINATE` keyword, then tries to `json.loads()` the response. The agent is prompted to respond in JSON, but LLMs sometimes wrap it in markdown code fences — so the function strips those too. If JSON parsing fails entirely it falls back to `{"raw": last_text}` so the API never crashes.

---

Now the API layer:**`app.py`** is the API layer — each section explained:

**Pydantic models** — `TradeRequest`, `TargetBreakdown`, `TradeSummary`, `TradeResponse` are not just data containers. FastAPI uses them for three things simultaneously: automatic JSON parsing of the incoming request body, input validation with clear error messages before your code even runs, and automatic OpenAPI/Swagger documentation generation. `model_config json_schema_extra` adds example queries that appear in the Swagger UI at `/docs`.

**`_inr(value)`** — a tiny helper that formats any float as `₹1,23,456.78`. Kept as a separate function so it can be reused across every row in the formatter without repeating the format string.

**`build_formatted_message(summary)`** — this takes a `TradeSummary` object and produces the aligned plain-text output. It has three branches: one target renders a vertical list, two targets renders a side-by-side comparison table using the `row()` inner function to keep column widths consistent, three or more targets renders a stacked block per target. The key design decision here is that formatting logic lives here — not in the agent prompt — because Python string formatting is reliable while LLM text alignment is not.

**`build_summary(data)`** — this is the bridge between the agent's dict and the Pydantic models. It handles three distinct dict shapes the agent can return: `{"error": ...}` returns `None, error_message`; `{"raw": ...}` returns `None, raw_text` as a graceful fallback; and a valid trade dict populates `TradeSummary`. The reason `summary` was `None` before is that this function never ran — `ask_agent` was returning a string and the `isinstance(result, dict)` check failed.

**`/trade` vs `/trade/text`** — two endpoints serving the same data differently. `/trade` returns JSON with both `summary` and `message` fields — ideal for a React frontend that wants to render cards from structured data. `/trade/text` returns `PlainTextResponse` — the string comes through with real newlines and alignment intact, ideal for a terminal, Telegram bot, or WhatsApp integration where you just want to `print()` the result.

**`async/await` everywhere** — `ask_agent` is `async` because `trading_team.run()` in AutoGen is a coroutine. FastAPI natively supports `async def` route handlers, so the whole chain is non-blocking — the server can handle other requests while waiting for Ollama to respond.
