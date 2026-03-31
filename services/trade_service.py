# services/trade_service.py

from models.trade import Trade


def calculate_trade(
    symbol: str,
    lots: int,
    buy_price: float,
    sell_price: float,
    stop_loss: float,
) -> dict:
    """
    Entry point for trade calculation.
    Instantiates Trade model and returns calculated result dict.
    """
    trade = Trade(
        symbol=symbol,
        lots=lots,
        buy_price=buy_price,
        sell_price=sell_price,
        stop_loss=stop_loss,
    )
    return trade.calculate()
