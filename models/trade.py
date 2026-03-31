# models/trade.py

from config.broker_config import symbol_config


class Trade:
    def __init__(self, symbol, lots, buy_price, sell_price, stop_loss):
        parts = symbol.strip().upper().split()

        if len(parts) != 3:
            raise ValueError(
                f"Invalid symbol format '{symbol}'. Expected: INDEX STRIKE CE/PE  e.g. 'NIFTY 18000 CE'"
            )

        self.index = parts[0]
        self.strike = float(parts[1])
        self.option_type = parts[2]

        if self.option_type not in ("CE", "PE"):
            raise ValueError("Option type must be CE or PE")

        if self.index not in symbol_config:
            raise ValueError(
                f"Invalid index '{self.index}'. Supported: {list(symbol_config.keys())}"
            )

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
        be = (
            self.strike + self.buy_price
            if self.option_type == "CE"
            else self.strike - self.buy_price
        )
        risk = (self.buy_price - self.stop_loss) * self.qty
        reward = (self.sell_price - self.buy_price) * self.qty
        loss_per_unit = self.buy_price - self.stop_loss
        total_loss = loss_per_unit * self.qty
        loss_with_charges = total_loss + charges

        return {
            "symbol": f"{self.index} {int(self.strike)} {self.option_type}",
            "lots": self.lots,
            "lot_size": self.lot_size,
            "qty": self.qty,
            "orders": self.orders,
            "buy_price": self.buy_price,
            "sell_price": self.sell_price,
            "stop_loss": self.stop_loss,
            "gross_profit": round(profit, 2),
            "charges": round(charges, 2),
            "net_profit": round(net_profit, 2),
            "investment": round(investment, 2),
            "profit_percent": round((net_profit / investment) * 100, 2) if investment else 0,
            "break_even": round(be, 2),
            "risk_reward": round(reward / risk, 2) if risk != 0 else 0,
            "loss_at_stoploss": round(total_loss, 2),
            "loss_with_charges": round(loss_with_charges, 2),
        }