from langchain.tools import tool
from services.trade_service import calculate_trade

@tool
def trade_calculator(
    symbol: str,
    lots: int,
    buy_price: float,
    sell_price: float,
    stop_loss: float
):
    """Calculate profit, loss, and risk for options trade"""
    try:
        return calculate_trade(symbol, lots, buy_price, sell_price, stop_loss)
    except Exception as e:
        return {"error": str(e)}