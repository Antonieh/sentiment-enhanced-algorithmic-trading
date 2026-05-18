from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from random import uniform


@dataclass
class LiveSignal:
    symbol: str
    signal_date: str
    sentiment_value: float   # S_t in [-1, 1]
    sentiment_strength: float  # M_t = |S_t|
    direction: int  # 1 buy, -1 sell, 0 hold


def map_sentiment_to_direction(s_t: float) -> int:
    if s_t > 0:
        return 1
    if s_t < 0:
        return -1
    return 0


def get_live_signal(symbol: str) -> LiveSignal:
    """
    Replace this mock with your real pipeline:
    1. collect latest RSS for symbol
    2. run FinBERT
    3. aggregate into S_t
    4. optionally combine with SMA filter
    """
    s_t = round(uniform(-0.8, 0.8), 3)  # placeholder
    m_t = abs(s_t)
    direction = map_sentiment_to_direction(s_t)

    return LiveSignal(
        symbol=symbol,
        signal_date=date.today().isoformat(),
        sentiment_value=s_t,
        sentiment_strength=m_t,
        direction=direction,
    )