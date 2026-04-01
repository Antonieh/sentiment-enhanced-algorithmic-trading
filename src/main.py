from src.strategies.baseline_sma import run_baseline_sma_strategy
from src.backtesting.trade_export import save_trade_table


def main() -> None:
    ticker = "AAPL"
    trades_df = run_baseline_sma_strategy(ticker)

    if trades_df.empty:
        print("No trades generated.")
    else:
        print(trades_df.head())
        save_trade_table(trades_df, ticker=ticker, strategy_name="baseline_sma")


if __name__ == "__main__":
    main()