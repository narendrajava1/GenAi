# tools/trade_tools.py

from services.trade_service import calculate_trade

# Words to strip from symbol
_ACTION_WORDS = {"BUY", "SELL", "SHORT", "LONG", "ABOVE", "BELOW", "AT"}


def _sanitize_symbol(symbol: str) -> str:
    """Strip action words from symbol. 'BUY NIFTY 22350 PE' → 'NIFTY 22350 PE'"""
    parts = symbol.strip().upper().split()
    return " ".join(p for p in parts if p not in _ACTION_WORDS)


# ── NOTE: AutoGen 0.4 tools are plain Python functions with type hints + docstrings
# ── The framework auto-registers them as tools via the @tool decorator or direct passing


def trade_calculator(
    symbol: str,
    lots: int,
    buy_price: float,
    sell_price: float,
    stop_loss: float,
) -> dict:
    """
    Calculate profit, loss, charges, risk-reward and break-even for a single target options trade.

    Args:
        symbol: Options symbol in format 'INDEX STRIKE CE/PE'. E.g. 'NIFTY 18000 CE', 'SENSEX 71900 PE'.
                Action words like BUY/SELL/ABOVE are stripped automatically.
        lots: Number of lots (integer)
        buy_price: Entry/buy price per unit (premium)
        sell_price: Target exit price per unit (premium)
        stop_loss: Stop loss price per unit (premium)

    Returns:
        dict with profit, loss, charges, investment, break_even, risk_reward, etc.
    """
    try:
        clean_symbol = _sanitize_symbol(symbol)
        return calculate_trade(clean_symbol, lots, buy_price, sell_price, stop_loss)
    except Exception as e:
        return {"error": str(e)}


def multi_target_calculator(
    symbol: str,
    lots: int,
    buy_price: float,
    targets: list,
    stop_loss: float,
) -> dict:
    """
    Calculate trade details for multiple target prices at once.
    Use this when the user gives more than one target, e.g. 'TARGET: 600 / 700'.

    Args:
        symbol: Options symbol in format 'INDEX STRIKE CE/PE'
        lots: Number of lots (integer)
        buy_price: Entry price per unit
        targets: List of target prices e.g. [600, 700]
        stop_loss: Stop loss price per unit

    Returns:
        dict with common trade fields + 'targets' list with per-target breakdown
    """
    try:
        clean_symbol = _sanitize_symbol(symbol)
        base = None
        results = []

        for target in targets:
            calc = calculate_trade(clean_symbol, lots, buy_price, target, stop_loss)
            if "error" in calc:
                return calc
            if base is None:
                base = calc
            results.append({
                "target": target,
                "gross_profit": calc["gross_profit"],
                "net_profit": calc["net_profit"],
                "profit_percent": calc["profit_percent"],
                "risk_reward": calc["risk_reward"],
                "charges": calc["charges"],
            })

        return {
            "symbol": base["symbol"],
            "lots": base["lots"],
            "lot_size": base["lot_size"],
            "qty": base["qty"],
            "orders": base["orders"],
            "buy_price": buy_price,
            "stop_loss": stop_loss,
            "investment": base["investment"],
            "break_even": base["break_even"],
            "loss_at_stoploss": base["loss_at_stoploss"],
            "loss_with_charges": base["loss_with_charges"],
            "charges": base["charges"],
            "targets": results,
        }
    except Exception as e:
        return {"error": str(e)}


def target_calculator(
    buy_price: float,
    sl: float,
    rr: float = 1.5,
) -> float:
    """
    Calculate suggested target price based on risk-reward ratio.

    Args:
        buy_price: Entry price of the option
        sl: Stop loss price
        rr: Risk-reward ratio (default 1.5 meaning 1:1.5)

    Returns:
        Suggested target price as float
    """
    try:
        risk = buy_price - sl
        target = buy_price + (risk * rr)
        return round(target, 2)
    except Exception as e:
        return {"error": str(e)}