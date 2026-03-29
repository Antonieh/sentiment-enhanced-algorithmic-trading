from pathlib import Path
import yaml

from src.data_collection.market_data import fetch_market_data
from src.data_collection.rss_news import fetch_rss_news


def load_tickers(config_path: str = "config/stocks.yaml") -> list[str]:
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config["stocks"]


def main() -> None:
    tickers = load_tickers()

    for ticker in tickers:
        print(f"Processing {ticker}...")
        fetch_market_data(ticker=ticker, start_date="2018-01-01", end_date="2024-12-31")
        fetch_rss_news(ticker=ticker)


if __name__ == "__main__":
    main()