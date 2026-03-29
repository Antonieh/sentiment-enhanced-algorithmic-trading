from src.sentiment.run_sentiment import run_finbert_for_ticker
from src.sentiment.aggregation import aggregate_daily_sentiment


def main() -> None:
    ticker = "AAPL"
    run_finbert_for_ticker(ticker)
    aggregate_daily_sentiment(ticker)


if __name__ == "__main__":
    main()