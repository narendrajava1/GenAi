from config.broker_config import symbol_config

class Trade:
    def __init__(self, symbol, lots, buy_price, sell_price, stop_loss):
        parts = symbol.split()

        if len(parts) != 3:
            raise ValueError("Invalid symbol format. Example: NIFTY 18000 CE")

        self.index = parts[0]
        self.strike = float(parts[1])
        self.option_type = parts[2]

        if self.index not in symbol_config:
            raise ValueError("Invalid index")

        config = symbol_config[self.index]

        self.lot_size = config["lot_size"]
        self.max_qty = config["max_qty"]

        self.lots = lots
        self.qty = lots * self.lot_size

        self.buy_price = buy_price
        self.sell_price = sell_price
        self.stop_loss = stop_loss

        self.orders = self.split_orders()

    def split_orders(self):
        orders = []
        remaining = self.qty

        while remaining > 0:
            order_qty = min(self.max_qty, remaining)
            orders.append(order_qty)
            remaining -= order_qty

        return orders

    def calculate(self):
        profit = sum((self.sell_price - self.buy_price) * o for o in self.orders)

        charges = sum(
            40 + ((self.buy_price + self.sell_price) * o * 0.0008)
            for o in self.orders
        )

        net_profit = profit - charges
        investment = self.buy_price * self.qty

        be = self.strike + self.buy_price if self.option_type == "CE" else self.strike - self.buy_price

        risk = (self.buy_price - self.stop_loss) * self.qty
        reward = (self.sell_price - self.buy_price) * self.qty

        loss_per_unit = self.buy_price - self.stop_loss
        total_loss = loss_per_unit * self.qty
        loss_with_charges = total_loss + charges

        return {
            "qty": self.qty,
            "orders": self.orders,
            "gross_profit": round(profit, 2),
            "charges": round(charges, 2),
            "net_profit": round(net_profit, 2),
            "investment": investment,
            "profit_percent": round((net_profit / investment) * 100, 2) if investment else 0,
            "break_even": be,
            "risk_reward": round(reward / risk, 2) if risk != 0 else 0,
            "loss_at_stoploss": round(total_loss, 2),
            "loss_with_charges": round(loss_with_charges, 2),
        }