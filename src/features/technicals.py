import pandas as pd


def add_sma_features(df: pd.DataFrame, short_window: int = 20, long_window: int = 50) -> pd.DataFrame:
    df = df.copy()

    if "Close" not in df.columns:
        raise ValueError("Expected 'Close' column in market data")

    df["sma_short"] = df["Close"].rolling(window=short_window, min_periods=short_window).mean()
    df["sma_long"] = df["Close"].rolling(window=long_window, min_periods=long_window).mean()

    return df