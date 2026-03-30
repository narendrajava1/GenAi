from fastapi import FastAPI
from pydantic import BaseModel

from ai.agent.agent_builder import build_agent
from ai.extractors.trade_extractor import extract_trade_data
from models.trade import Trade

app = FastAPI()
agent=build_agent()


class QueryRequest(BaseModel):
    query: str

# Request body
class TradeRequest(BaseModel):
    symbol: str
    lots: int
    buy_price: float
    sell_price: float
    stop_loss: float
@app.get("/")
def home():
    return {"message": "Trading API is running 🚀"}

@app.post("/calculate")
def calculate_trade(data: TradeRequest):
    trade = Trade(
        data.symbol,
        data.lots,
        data.buy_price,
        data.sell_price,
        data.stop_loss
    )

    return trade.calculate()

@app.get("/ai")
def home():
    return {"message": "AI Trading Agent 🚀"}

@app.post("/ai/calculate")
def ai_trade(data: QueryRequest):
    try:
        extracted = extract_trade_data(data.query)

        required = ["symbol", "lots", "buy_price", "sell_price", "stop_loss"]

        for field in required:
            if field not in extracted:
                return {
                    "error": f"Missing field: {field}",
                    "extracted": extracted
                }

        # ✅ FIX HERE
        trade = Trade(
            extracted["symbol"],
            extracted["lots"],
            extracted["buy_price"],
            extracted["sell_price"],
            extracted["stop_loss"]
        )

        result = trade.calculate()

        return {
            "input": extracted,
            "result": result
        }

    except Exception as e:
        return {"error": str(e)}