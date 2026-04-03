from src.strategies.baseline_sma import run_baseline_sma_strategy
from src.strategies.sentiment_sma import run_sentiment_sma_strategy
from src.backtesting.trade_export import save_trade_table
from src.analysis.metrics import compute_trade_metrics, save_metrics


def main() -> None:
    ticker = "AAPL"

    baseline_trades = run_baseline_sma_strategy(ticker)
    if baseline_trades.empty:
        print("No baseline trades generated.")
    else:
        print("Baseline trades:")
        print(baseline_trades.head())
        save_trade_table(baseline_trades, ticker=ticker, strategy_name="baseline_sma")
        baseline_metrics = compute_trade_metrics(baseline_trades)
        print("Baseline metrics:")
        print(baseline_metrics)
        save_metrics(baseline_metrics, ticker=ticker, strategy_name="baseline_sma")

    sentiment_trades = run_sentiment_sma_strategy(ticker)
    if sentiment_trades.empty:
        print("No sentiment-filtered trades generated.")
    else:
        print("Sentiment-filtered trades:")
        print(sentiment_trades.head())
        save_trade_table(sentiment_trades, ticker=ticker, strategy_name="sentiment_sma")
        sentiment_metrics = compute_trade_metrics(sentiment_trades)
        print("Sentiment metrics:")
        print(sentiment_metrics)
        save_metrics(sentiment_metrics, ticker=ticker, strategy_name="sentiment_sma")


if __name__ == "__main__":
    main()