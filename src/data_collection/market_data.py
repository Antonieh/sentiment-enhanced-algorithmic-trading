from pathlib import Path

import pandas as pd
import yfinance as yf


def fetch_market_data(ticker: str, start_date: str, end_date: str) -> Path:
    output_dir = Path("data/raw/market")
    output_dir.mkdir(parents=True, exist_ok=True)

    df = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=False,
        progress=False,
    )

    if df.empty:
        raise ValueError(f"No market data returned for {ticker}")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    df = df.reset_index()

    expected_cols = ["Date", "Adj Close", "Close", "High", "Low", "Open", "Volume"]
    missing = [col for col in expected_cols if col not in df.columns]
    if missing:
        raise ValueError(
            f"Missing expected OHLCV columns for {ticker}: {missing}. "
            f"Found columns: {df.columns.tolist()}"
        )

    df = df[expected_cols]

    output_path = output_dir / f"{ticker}_ohlcv.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved market data for {ticker} to {output_path}")
    return output_path