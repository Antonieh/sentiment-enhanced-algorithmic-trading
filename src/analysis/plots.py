from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def plot_equity_curve(trades_df: pd.DataFrame, ticker: str, strategy_name: str) -> Path:
    output_dir = Path("data/processed/plots")
    output_dir.mkdir(parents=True, exist_ok=True)

    if trades_df.empty:
        raise ValueError("Cannot plot equity curve from empty trade table")

    df = trades_df.copy()
    df["exit_time"] = pd.to_datetime(df["exit_time"], errors="coerce")
    df["return_pct"] = pd.to_numeric(df["return_pct"], errors="coerce").fillna(0.0)
    df = df.sort_values("exit_time")

    df["equity_curve"] = (1 + df["return_pct"]).cumprod()

    plt.figure(figsize=(10, 5))
    plt.plot(df["exit_time"], df["equity_curve"])
    plt.xlabel("Exit Time")
    plt.ylabel("Equity")
    plt.title(f"Equity Curve - {ticker} - {strategy_name}")
    plt.tight_layout()

    output_path = output_dir / f"{ticker}_{strategy_name}_equity_curve.png"
    plt.savefig(output_path)
    plt.close()

    print(f"Saved equity curve to {output_path}")
    return output_path


def plot_balance_curve(trades_df: pd.DataFrame, ticker: str, strategy_name: str, starting_balance: float = 1.0) -> Path:
    output_dir = Path("data/processed/plots")
    output_dir.mkdir(parents=True, exist_ok=True)

    if trades_df.empty:
        raise ValueError("Cannot plot balance curve from empty trade table")

    df = trades_df.copy()
    df["exit_time"] = pd.to_datetime(df["exit_time"], errors="coerce")
    df["pnl"] = pd.to_numeric(df["pnl"], errors="coerce").fillna(0.0)
    df = df.sort_values("exit_time")

    df["balance_curve"] = starting_balance + df["pnl"].cumsum()

    plt.figure(figsize=(10, 5))
    plt.plot(df["exit_time"], df["balance_curve"])
    plt.xlabel("Exit Time")
    plt.ylabel("Balance")
    plt.title(f"Balance Curve - {ticker} - {strategy_name}")
    plt.tight_layout()

    output_path = output_dir / f"{ticker}_{strategy_name}_balance_curve.png"
    plt.savefig(output_path)
    plt.close()

    print(f"Saved balance curve to {output_path}")
    return output_path