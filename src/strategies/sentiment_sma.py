from pathlib import Path
import pandas as pd


def run_sentiment_sma_strategy(ticker: str) -> pd.DataFrame:
    input_path = Path("data/processed/merged") / f"{ticker}_merged.csv"

    if not input_path.exists():
        raise FileNotFoundError(f"Missing merged dataset: {input_path}")

    df = pd.read_csv(input_path)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"]).copy()

    required_cols = ["Date", "Close", "sma_short", "sma_long", "S_t", "M_t"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for sentiment strategy: {missing}")

    df["position_signal"] = 0

    df.loc[
        (df["sma_short"] > df["sma_long"]) &
        (df["sma_short"].shift(1) <= df["sma_long"].shift(1)) &
        (df["S_t"] > 0),
        "position_signal"
    ] = 1

    df.loc[
        (df["sma_short"] < df["sma_long"]) &
        (df["sma_short"].shift(1) >= df["sma_long"].shift(1)),
        "position_signal"
    ] = -1

    trades = []
    in_position = False
    entry_row = None

    for _, row in df.iterrows():
        signal = row["position_signal"]

        if signal == 1 and not in_position:
            in_position = True
            entry_row = row

        elif signal == -1 and in_position and entry_row is not None:
            trade = {
                "ticker": ticker,
                "strategy": "sentiment_sma",
                "entry_time": entry_row["Date"],
                "exit_time": row["Date"],
                "entry_price": float(entry_row["Close"]),
                "exit_price": float(row["Close"]),
                "side": "long",
                "pnl": float(row["Close"] - entry_row["Close"]),
                "return_pct": float((row["Close"] - entry_row["Close"]) / entry_row["Close"]),
                "sma_short_entry": float(entry_row["sma_short"]),
                "sma_long_entry": float(entry_row["sma_long"]),
                "S_t_entry": float(entry_row["S_t"]),
                "M_t_entry": float(entry_row["M_t"]),
            }
            trades.append(trade)
            in_position = False
            entry_row = None

    return pd.DataFrame(trades)