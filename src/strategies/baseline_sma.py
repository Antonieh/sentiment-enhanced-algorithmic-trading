from pathlib import Path
import pandas as pd

EVAL_START = pd.Timestamp("2026-04-02")
EVAL_END = pd.Timestamp("2026-04-30")


def run_baseline_sma_strategy(ticker: str) -> pd.DataFrame:
    input_path = Path("data/processed/merged") / f"{ticker}_merged.csv"

    if not input_path.exists():
        raise FileNotFoundError(f"Missing merged dataset: {input_path}")

    df = pd.read_csv(input_path)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"]).copy()

    required_cols = ["Date", "Close", "sma_short", "sma_long"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for baseline strategy: {missing}")

    df = df[(df["Date"] >= EVAL_START) & (df["Date"] <= EVAL_END)].copy()
    df = df.sort_values("Date").reset_index(drop=True)

    if len(df) < 2:
        return pd.DataFrame()

    df["signal"] = 0
    df.loc[df["sma_short"] > df["sma_long"], "signal"] = 1
    df.loc[df["sma_short"] < df["sma_long"], "signal"] = -1

    trades = []

    for i in range(len(df) - 1):
        row = df.iloc[i]
        next_row = df.iloc[i + 1]

        if row["signal"] == 1:
            trades.append({
                "ticker": ticker,
                "strategy": "baseline_sma",
                "entry_time": pd.Timestamp(row["Date"]),
                "exit_time": pd.Timestamp(next_row["Date"]),
                "entry_price": float(row["Close"]),
                "exit_price": float(next_row["Close"]),
                "side": "long",
                "signal_used": "bullish_sma",
                "sma_short_entry": float(row["sma_short"]),
                "sma_long_entry": float(row["sma_long"]),
                "pnl": float(next_row["Close"] - row["Close"]),
                "return_pct": float((next_row["Close"] - row["Close"]) / row["Close"]),
            })

        elif row["signal"] == -1:
            trades.append({
                "ticker": ticker,
                "strategy": "baseline_sma",
                "entry_time": pd.Timestamp(row["Date"]),
                "exit_time": pd.Timestamp(next_row["Date"]),
                "entry_price": float(row["Close"]),
                "exit_price": float(next_row["Close"]),
                "side": "short",
                "signal_used": "bearish_sma",
                "sma_short_entry": float(row["sma_short"]),
                "sma_long_entry": float(row["sma_long"]),
                "pnl": float(row["Close"] - next_row["Close"]),
                "return_pct": float((row["Close"] - next_row["Close"]) / row["Close"]),
            })

    return pd.DataFrame(trades)