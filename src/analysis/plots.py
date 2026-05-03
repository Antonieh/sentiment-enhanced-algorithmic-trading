from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

SHARES = 10


def _prepare_trades(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["exit_time"] = pd.to_datetime(df["exit_time"])
    df["entry_price"] = pd.to_numeric(df["entry_price"])
    df["exit_price"] = pd.to_numeric(df["exit_price"])
    df["side"] = df["side"].astype(str).str.lower().str.strip()

    df = df.sort_values("exit_time").reset_index(drop=True)

    def compute_pnl(row):
        if row["side"] == "long":
            return SHARES * (row["exit_price"] - row["entry_price"])
        elif row["side"] == "short":
            return SHARES * (row["entry_price"] - row["exit_price"])
        return 0.0

    df["pnl_fixed"] = df.apply(compute_pnl, axis=1)

    print("\nDEBUG PnL:")
    print(df[["entry_price", "exit_price", "side", "pnl_fixed"]])

    return df


def plot_balance_curve(trades_df, ticker, strategy_name, starting_balance=10000):
    df = _prepare_trades(trades_df)

    df["balance"] = starting_balance + df["pnl_fixed"].cumsum()

    print("\nDEBUG BALANCE:")
    print(df[["exit_time", "pnl_fixed", "balance"]])

    plt.figure(figsize=(10, 5))
    plt.plot(df["exit_time"], df["balance"], marker="o")

    plt.title(f"Balance Curve - {ticker} - {strategy_name}")
    plt.xlabel("Exit Time")
    plt.ylabel("Balance")

    output_path = Path("data/processed/plots") / f"{ticker}_{strategy_name}_balance.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(output_path)
    plt.close()

    print("Saved:", output_path)