# config/broker_config.py

symbol_config = {
    "NIFTY": {
        "lot_size": 65,
        "max_qty": 1755,   # max qty per order (exchange limit)
    },
    "BANKNIFTY": {
        "lot_size": 15,
        "max_qty": 900,
    },
    "FINNIFTY": {
        "lot_size": 40,
        "max_qty": 1800,
    },
    "MIDCPNIFTY": {
        "lot_size": 75,
        "max_qty": 2100,
    },
    "SENSEX": {
        "lot_size": 20,
        "max_qty": 1000,
    },
}
