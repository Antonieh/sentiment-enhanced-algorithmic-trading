from pathlib import Path
import pandas as pd


def save_trade_table(trades_df: pd.DataFrame, ticker: str, strategy_name: str) -> None:
    output_dir = Path("data/processed/trade_tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{ticker}_{strategy_name}_trades.csv"
    trades_df.to_csv(output_path, index=False)

    print(f"Saved trade table to {output_path}")