from pathlib import Path

import yfinance as yf


def fetch_market_data(ticker: str, start_date: str, end_date: str) -> None:
    output_dir = Path("data/raw/market")
    output_dir.mkdir(parents=True, exist_ok=True)

    df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)

    if df.empty:
        raise ValueError(f"No market data returned for {ticker}")

    output_path = output_dir / f"{ticker}_ohlcv.csv"
    df.to_csv(output_path)

    print(f"Saved market data for {ticker} to {output_path}")