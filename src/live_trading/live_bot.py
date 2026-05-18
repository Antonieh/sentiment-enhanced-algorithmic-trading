from __future__ import annotations

from src.sentiment.live_signal_provider import get_live_signal
from src.live_trading.mt5_runner import (
    initialize_mt5,
    shutdown_mt5,
    ensure_symbol,
    has_open_position,
    place_order,
)

# Use the exact symbol names from your broker
SYMBOLS = [
    "AAPL",
    "NVDA",
    "AMD",
    "AMZN",
    "NFLX",
    "AXP",
    "DELL",
    "CAT",
    "JNJ",
    "XOM",
]

# sentiment strength thresholds
WEAK_THRESHOLD = 0.10
MEDIUM_THRESHOLD = 0.25
STRONG_THRESHOLD = 0.45


def choose_lot(m_t: float) -> float:
    if m_t < WEAK_THRESHOLD:
        return 0.0
    if m_t < MEDIUM_THRESHOLD:
        return 0.01
    if m_t < STRONG_THRESHOLD:
        return 0.02
    return 0.03


def run_live_bot():
    if not initialize_mt5():
        return

    try:
        for symbol in SYMBOLS:
            print(f"\n--- {symbol} ---")

            if not ensure_symbol(symbol):
                continue

            signal = get_live_signal(symbol)
            print(
                f"{symbol} | date={signal.signal_date} | "
                f"S_t={signal.sentiment_value:.4f} | "
                f"M_t={signal.sentiment_strength:.4f} | "
                f"direction={signal.direction}"
            )

            if has_open_position(symbol):
                print(f"{symbol}: position already open, skipping")
                continue

            lot = choose_lot(signal.sentiment_strength)
            if lot <= 0:
                print(f"{symbol}: sentiment too weak, no trade")
                continue

            if signal.direction == 1:
                place_order(symbol, "BUY", lot, comment=f"sent_{signal.sentiment_strength:.2f}")
            elif signal.direction == -1:
                place_order(symbol, "SELL", lot, comment=f"sent_{signal.sentiment_strength:.2f}")
            else:
                print(f"{symbol}: neutral signal, no trade")

    finally:
        shutdown_mt5()