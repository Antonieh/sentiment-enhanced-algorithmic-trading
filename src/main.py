from src.strategies.baseline_sma import run_baseline_sma_strategy
from src.backtesting.trade_export import save_trade_table
from src.analysis.metrics import compute_trade_metrics, save_metrics
from src.analysis.signal_strength_analysis import (
    analyze_signal_strength,
    save_signal_strength_analysis,
)


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

        strength_df = analyze_signal_strength(baseline_trades)
        print("Signal strength analysis:")
        print(strength_df)
        save_signal_strength_analysis(strength_df, ticker=ticker, strategy_name="baseline_sma")


if __name__ == "__main__":
    main()