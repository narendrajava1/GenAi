from langchain.tools import tool


@tool
def target_calculator(buy_price: float, sl: float, rr: float = 1.5)-> float:
    """
        Calculate target price based on risk-reward ratio.

        buy_price: entry price of option
        sl: stop loss price
        rr: risk reward ratio (default 1.5)
        """
    risk = buy_price - sl
    target = buy_price + (risk * rr)
    return round(target, 2)