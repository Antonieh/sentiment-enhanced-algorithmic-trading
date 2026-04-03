from pathlib import Path
import pandas as pd

from src.analysis.plots import plot_equity_curve, plot_balance_curve


def main() -> None:
    ticker = "AAPL"
    strategy_name = "baseline_sma"
    trade_path = Path("data/processed/trade_tables") / f"{ticker}_{strategy_name}_trades.csv"

    if not trade_path.exists():
        raise FileNotFoundError(f"Missing trade table: {trade_path}")

    trades_df = pd.read_csv(trade_path)

    plot_equity_curve(trades_df, ticker=ticker, strategy_name=strategy_name)
    plot_balance_curve(trades_df, ticker=ticker, strategy_name=strategy_name, starting_balance=10000.0)


if __name__ == "__main__":
    main()