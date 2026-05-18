from __future__ import annotations

from typing import Optional
import MetaTrader5 as mt5

from config.live_config import LiveConfig


def initialize_mt5() -> bool:
    if not mt5.initialize():
        print("MT5 initialize failed:", mt5.last_error())
        return False
    return True


def shutdown_mt5() -> None:
    mt5.shutdown()


def ensure_symbol(symbol: str) -> bool:
    if not mt5.symbol_select(symbol, True):
        print(f"Failed to select symbol: {symbol}")
        return False
    return True


def get_tick(symbol: str):
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print(f"No tick data for {symbol}")
    return tick


def has_open_mt5_position(symbol: str) -> bool:
    positions = mt5.positions_get(symbol=symbol)
    return positions is not None and len(positions) > 0


def send_market_order(symbol: str, side: str, lot: float, comment: str = "live_bot"):
    tick = get_tick(symbol)
    if tick is None:
        return None

    if side.upper() == "BUY":
        price = tick.ask
        order_type = mt5.ORDER_TYPE_BUY
    elif side.upper() == "SELL":
        price = tick.bid
        order_type = mt5.ORDER_TYPE_SELL
    else:
        raise ValueError("side must be BUY or SELL")

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "deviation": LiveConfig.DEVIATION,
        "magic": LiveConfig.MAGIC_NUMBER,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    print(f"{symbol} {side} result:", result)
    return result


def close_position(symbol: str):
    positions = mt5.positions_get(symbol=symbol)
    if positions is None or len(positions) == 0:
        print(f"No open MT5 position to close for {symbol}")
        return None

    position = positions[0]
    tick = get_tick(symbol)
    if tick is None:
        return None

    if position.type == mt5.POSITION_TYPE_BUY:
        close_type = mt5.ORDER_TYPE_SELL
        price = tick.bid
    else:
        close_type = mt5.ORDER_TYPE_BUY
        price = tick.ask

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": position.volume,
        "type": close_type,
        "position": position.ticket,
        "price": price,
        "deviation": LiveConfig.DEVIATION,
        "magic": LiveConfig.MAGIC_NUMBER,
        "comment": "time_exit",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    print(f"{symbol} CLOSE result:", result)
    return result