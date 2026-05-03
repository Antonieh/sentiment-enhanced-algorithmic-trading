from src.strategies.baseline_sma import run_baseline_sma_strategy
from src.strategies.sentiment_sma import run_sentiment_sma_strategy
from src.backtesting.trade_export import save_trade_table
from src.analysis.metrics import compute_trade_metrics, save_metrics
from src.analysis.signal_strength_analysis import (
    analyze_signal_strength,
    save_signal_strength_analysis,
)


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


def run_one_strategy(ticker: str, strategy_name: str):
    if strategy_name == "baseline_sma":
        trades_df = run_baseline_sma_strategy(ticker)
    elif strategy_name == "sentiment_sma":
        trades_df = run_sentiment_sma_strategy(ticker)
    else:
        raise ValueError(f"Unknown strategy: {strategy_name}")

    save_trade_table(trades_df, ticker=ticker, strategy_name=strategy_name)

    metrics_df = compute_trade_metrics(trades_df)
    save_metrics(metrics_df, ticker=ticker, strategy_name=strategy_name)

    if strategy_name == "sentiment_sma" and "M_t_entry" in trades_df.columns:
        strength_df = analyze_signal_strength(trades_df)
        save_signal_strength_analysis(
            strength_df,
            ticker=ticker,
            strategy_name=strategy_name,
        )

    if trades_df.empty:
        print(f"No trades generated for {ticker} using {strategy_name}")
    else:
        print(f"Completed {strategy_name} for {ticker}")


def main() -> None:
    for ticker in TICKERS:
        print(f"\n=== Running experiments for {ticker} ===")

        try:
            run_one_strategy(ticker, "baseline_sma")
        except Exception as e:
            print(f"Baseline strategy error for {ticker}: {e}")

        try:
            run_one_strategy(ticker, "sentiment_sma")
        except Exception as e:
            print(f"Sentiment strategy error for {ticker}: {e}")


if __name__ == "__main__":
    main()