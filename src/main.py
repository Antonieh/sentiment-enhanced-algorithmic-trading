from src.features.merge_data import merge_market_and_sentiment


def main() -> None:
    merge_market_and_sentiment("AAPL")


if __name__ == "__main__":
    main()