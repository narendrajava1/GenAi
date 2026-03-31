# tools/trade_tools.py

from langchain.tools import tool
from services.trade_service import calculate_trade


@tool
def trade_calculator(
    symbol: str,
    lots: int,
    buy_price: float,
    sell_price: float,
    stop_loss: float,
) -> dict:
    """
    Calculate profit, loss, charges, risk-reward and break-even for an options trade.

    Args:
        symbol    : Options symbol in format 'INDEX STRIKE CE/PE'
                    Examples: 'NIFTY 18000 CE', 'BANKNIFTY 44000 PE'
        lots      : Number of lots (integer, e.g. 1, 2, 5)
        buy_price : Premium paid to enter the trade (per unit)
        sell_price: Target premium at which to exit (per unit)
        stop_loss : Stop loss premium level (per unit)

    Returns:
        dict with keys: qty, orders, gross_profit, charges, net_profit,
        investment, profit_percent, break_even, risk_reward,
        loss_at_stoploss, loss_with_charges
    """
    try:
        return calculate_trade(symbol, lots, buy_price, sell_price, stop_loss)
    except Exception as e:
        return {"error": str(e)}
