from dataclasses import dataclass

@dataclass(frozen=True)
class LiveConfig:
    MAGIC_NUMBER: int = 123456
    DEVIATION: int = 10
    DEFAULT_LOT: float = 0.01
    MAX_LOT: float = 0.05
    STATE_FILE: str = "data/live_positions.json"

    # Replace with your exact MT5 broker symbols
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

    # Sentiment strength thresholds based on M_t = |S_t|
    WEAK_THRESHOLD: float = 0.10
    MEDIUM_THRESHOLD: float = 0.25
    STRONG_THRESHOLD: float = 0.45

    # Example holding periods by sentiment strength
    WEAK_HOLD_DAYS: int = 1
    MEDIUM_HOLD_DAYS: int = 2
    STRONG_HOLD_DAYS: int = 3