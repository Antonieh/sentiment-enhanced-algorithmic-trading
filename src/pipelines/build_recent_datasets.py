from src.data_collection.market_data import fetch_market_data
from src.features.merge_data import merge_market_and_sentiment


TICKERS = [
    "AAPL",
    "AMZN",
    "AMD",
    "AXP",
    "CAT",
    "DELL",
    "JNJ",
    "NFLX",
    "NVDA",
    "XOM",
]


def main() -> None:
    for ticker in TICKERS:
        try:
            print(f"\n--- Building dataset for {ticker} ---")
            fetch_market_data(
                ticker=ticker,
                start_date="2025-01-01",
                end_date="2026-12-31",
            )
            merge_market_and_sentiment(
                ticker=ticker,
                short_window=20,
                long_window=50,
            )
        except Exception as e:
            print(f"Error building dataset for {ticker}: {e}")


if __name__ == "__main__":
    main()