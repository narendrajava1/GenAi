from langchain.tools import tool

@tool
def position_size(capital: float, risk_percent: float, stop_loss: float):
    """Calculate position size based on risk"""
    risk_amount = capital * (risk_percent / 100)
    qty = risk_amount / stop_loss
    return {"recommended_qty": int(qty)}