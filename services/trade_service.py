from models.trade import Trade

def calculate_trade(symbol, lots, buy_price, sell_price, stop_loss):
    trade = Trade(symbol, lots, buy_price, sell_price, stop_loss)
    return trade.calculate()