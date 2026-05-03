from pathlib import Path
import pandas as pd

from src.analysis.plots import plot_balance_curve


def main() -> None:
    summary_path = Path("data/processed/metrics/sentiment_sma_summary.csv")
    trade_dir = Path("data/processed/trade_tables")

    if not summary_path.exists():
        raise FileNotFoundError(f"Missing summary file: {summary_path}")

    if not trade_dir.exists():
        raise FileNotFoundError(f"Missing trade table directory: {trade_dir}")

    summary_df = pd.read_csv(summary_path)

    if summary_df.empty:
        raise ValueError("Sentiment summary is empty")

    summary_df = summary_df.sort_values(
        by=["sharpe_ratio", "profit_factor", "cumulative_return"],
        ascending=False,
    )

    for _, row in summary_df.iterrows():
        ticker = row["ticker"]
        strategy_name = row["strategy"]

        trade_path = trade_dir / f"{ticker}_{strategy_name}_trades.csv"
        if not trade_path.exists():
            print(f"Missing trade table for {ticker} {strategy_name}")
            continue

        trades_df = pd.read_csv(trade_path)

        if trades_df.empty:
            print(f"Skipping empty trade table: {trade_path.name}")
            continue

        print(f"Plotting {ticker} - {strategy_name}")
        plot_balance_curve(
            trades_df,
            ticker=ticker,
            strategy_name=strategy_name,
            starting_balance=10000.0,
        )


if __name__ == "__main__":
    main()