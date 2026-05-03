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

    required_cols = ["Date", "Close", "S_t", "M_t"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for sentiment strategy: {missing}")

    df = df[(df["Date"] >= EVAL_START) & (df["Date"] <= EVAL_END)].copy()
    df = df.sort_values("Date").reset_index(drop=True)

    if len(df) < 2:
        return pd.DataFrame()

    trades = []

    for i in range(len(df) - 1):
        row = df.iloc[i]
        next_row = df.iloc[i + 1]

        if row["S_t"] > SENTIMENT_THRESHOLD:
            trades.append({
                "ticker": ticker,
                "strategy": "sentiment_daily",
                "entry_time": pd.Timestamp(row["Date"]),
                "exit_time": pd.Timestamp(next_row["Date"]),
                "entry_price": float(row["Close"]),
                "exit_price": float(next_row["Close"]),
                "side": "long",
                "pnl": float(next_row["Close"] - row["Close"]),
                "return_pct": float((next_row["Close"] - row["Close"]) / row["Close"]),
                "S_t_entry": float(row["S_t"]),
                "M_t_entry": float(row["M_t"]),
            })

        elif row["S_t"] < -SENTIMENT_THRESHOLD:
            trades.append({
                "ticker": ticker,
                "strategy": "sentiment_daily",
                "entry_time": pd.Timestamp(row["Date"]),
                "exit_time": pd.Timestamp(next_row["Date"]),
                "entry_price": float(row["Close"]),
                "exit_price": float(next_row["Close"]),
                "side": "short",
                "pnl": float(row["Close"] - next_row["Close"]),
                "return_pct": float((row["Close"] - next_row["Close"]) / row["Close"]),
                "S_t_entry": float(row["S_t"]),
                "M_t_entry": float(row["M_t"]),
            })

    return pd.DataFrame(trades)