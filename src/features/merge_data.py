from pathlib import Path
import pandas as pd

from src.features.technicals import add_sma_features


def merge_market_and_sentiment(ticker: str) -> None:
    market_path = Path("data/raw/market") / f"{ticker}_ohlcv.csv"
    sentiment_path = Path("data/processed/sentiment") / f"{ticker}_daily_sentiment.csv"
    output_dir = Path("data/processed/merged")
    output_dir.mkdir(parents=True, exist_ok=True)

    if not market_path.exists():
        raise FileNotFoundError(f"Missing market data file: {market_path}")

    if not sentiment_path.exists():
        raise FileNotFoundError(f"Missing daily sentiment file: {sentiment_path}")

    # Yahoo export currently has 3 extra header rows:
    # Price / Ticker / Date
    market_df = pd.read_csv(
        market_path,
        skiprows=3,
        names=["Date", "Adj Close", "Close", "High", "Low", "Open", "Volume"],
    )

    sentiment_df = pd.read_csv(sentiment_path)

    market_df["Date"] = pd.to_datetime(market_df["Date"], errors="coerce").dt.date
    market_df = market_df.dropna(subset=["Date"])

    # Make sure numeric columns are numeric
    for col in ["Adj Close", "Close", "High", "Low", "Open", "Volume"]:
        market_df[col] = pd.to_numeric(market_df[col], errors="coerce")

    if "date" not in sentiment_df.columns:
        raise ValueError(f"Could not find 'date' column in sentiment data. Columns: {sentiment_df.columns.tolist()}")

    sentiment_df["date"] = pd.to_datetime(sentiment_df["date"], errors="coerce").dt.date
    sentiment_df = sentiment_df.dropna(subset=["date"])

    market_df = add_sma_features(market_df, short_window=20, long_window=50)

    merged_df = market_df.merge(
        sentiment_df[["date", "S_t", "M_t", "n_articles"]],
        how="left",
        left_on="Date",
        right_on="date",
    )

    merged_df["S_t"] = merged_df["S_t"].fillna(0.0)
    merged_df["M_t"] = merged_df["M_t"].fillna(0.0)
    merged_df["n_articles"] = merged_df["n_articles"].fillna(0).astype(int)

    merged_df["ticker"] = ticker

    output_path = output_dir / f"{ticker}_merged.csv"
    merged_df.to_csv(output_path, index=False)

    print(f"Saved merged dataset for {ticker} to {output_path}")