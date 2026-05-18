import MetaTrader5 as mt5


def place_order(symbol, order_type="BUY", lot=0.01):
    if not mt5.initialize():
        print("MT5 init failed:", mt5.last_error())
        return None

    if not mt5.symbol_select(symbol, True):
        print(f"Failed to select {symbol}")
        mt5.shutdown()
        return None

    tick = mt5.symbol_info_tick(symbol)

    if order_type == "BUY":
        price = tick.ask
        order_type_mt5 = mt5.ORDER_TYPE_BUY
    else:
        price = tick.bid
        order_type_mt5 = mt5.ORDER_TYPE_SELL

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type_mt5,
        "price": price,
        "deviation": 10,
        "magic": 123456,
        "comment": "bot trade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)

    print("Order result:", result)

    mt5.shutdown()
    return result