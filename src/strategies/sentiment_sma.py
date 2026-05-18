from pathlib import Path
import pandas as pd

EVAL_START = pd.Timestamp("2026-04-02")
EVAL_END = pd.Timestamp("2026-04-30")
SENTIMENT_THRESHOLD = 0.05


def run_sentiment_sma_strategy(ticker: str) -> pd.DataFrame:
    input_path = Path("data/processed/merged") / f"{ticker}_merged.csv"

    if not input_path.exists():
        raise FileNotFoundError(f"Missing merged dataset: {input_path}")

    df = pd.read_csv(input_path)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"]).copy()

    required_cols = [
        "Date",
        "Close",
        "sma_short",
        "sma_long",
        "S_t",
        "M_t",
    ]

    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required columns for sentiment SMA strategy: {missing}"
        )

    df = df[(df["Date"] >= EVAL_START) & (df["Date"] <= EVAL_END)].copy()
    df = df.sort_values("Date").reset_index(drop=True)

    if len(df) < 3:
        return pd.DataFrame()

    trades = []

    for i in range(1, len(df) - 1):
        prev_row = df.iloc[i - 1]
        row = df.iloc[i]
        next_row = df.iloc[i + 1]

        bullish_cross = (
            row["sma_short"] > row["sma_long"]
            and prev_row["sma_short"] <= prev_row["sma_long"]
        )

        bearish_cross = (
            row["sma_short"] < row["sma_long"]
            and prev_row["sma_short"] >= prev_row["sma_long"]
        )

        positive_sentiment = row["S_t"] > SENTIMENT_THRESHOLD
        negative_sentiment = row["S_t"] < -SENTIMENT_THRESHOLD

        if bullish_cross and positive_sentiment:
            trades.append({
                "ticker": ticker,
                "strategy": "sentiment_sma",
                "entry_time": pd.Timestamp(row["Date"]),
                "exit_time": pd.Timestamp(next_row["Date"]),
                "entry_price": float(row["Close"]),
                "exit_price": float(next_row["Close"]),
                "side": "long",
                "signal_used": "bullish_sma_positive_sentiment",
                "sma_short_entry": float(row["sma_short"]),
                "sma_long_entry": float(row["sma_long"]),
                "S_t_entry": float(row["S_t"]),
                "M_t_entry": float(row["M_t"]),
                "pnl": float(next_row["Close"] - row["Close"]),
                "return_pct": float(
                    (next_row["Close"] - row["Close"]) / row["Close"]
                ),
            })

        elif bearish_cross and negative_sentiment:
            trades.append({
                "ticker": ticker,
                "strategy": "sentiment_sma",
                "entry_time": pd.Timestamp(row["Date"]),
                "exit_time": pd.Timestamp(next_row["Date"]),
                "entry_price": float(row["Close"]),
                "exit_price": float(next_row["Close"]),
                "side": "short",
                "signal_used": "bearish_sma_negative_sentiment",
                "sma_short_entry": float(row["sma_short"]),
                "sma_long_entry": float(row["sma_long"]),
                "S_t_entry": float(row["S_t"]),
                "M_t_entry": float(row["M_t"]),
                "pnl": float(row["Close"] - next_row["Close"]),
                "return_pct": float(
                    (row["Close"] - next_row["Close"]) / row["Close"]
                ),
            })

    return pd.DataFrame(trades)