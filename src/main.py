from src.data_collection.rss_news import fetch_rss_news
from src.sentiment.run_sentiment import score_rss_news_file


def main() -> None:
    ticker = "AAPL"
    fetch_rss_news(ticker=ticker, limit=20)
    score_rss_news_file(ticker=ticker)


if __name__ == "__main__":
    main()