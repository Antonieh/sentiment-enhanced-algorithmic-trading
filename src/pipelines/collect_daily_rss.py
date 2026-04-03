from src.data_collection.rss_news import fetch_rss_news
from src.sentiment.run_sentiment import score_rss_news_file
from src.sentiment.aggregation import aggregate_daily_sentiment


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
            print(f"\n--- Processing {ticker} ---")
            fetch_rss_news(ticker=ticker, limit=20)
            score_rss_news_file(ticker=ticker)
            aggregate_daily_sentiment(ticker=ticker)
        except Exception as e:
            print(f"Error processing {ticker}: {e}")


if __name__ == "__main__":
    main()