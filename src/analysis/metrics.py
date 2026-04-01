from pathlib import Path
import pandas as pd
import numpy as np


def compute_trade_metrics(trades_df: pd.DataFrame) -> pd.DataFrame:
    if trades_df.empty:
        return pd.DataFrame(
            [
                {
                    "total_trades": 0,
                    "winning_rate": 0.0,
                    "profit_factor": 0.0,
                    "average_trade_return": 0.0,
                    "cumulative_return": 0.0,
                    "max_drawdown": 0.0,
                    "sharpe_ratio": 0.0,
                }
            ]
        )

    df = trades_df.copy()

    df["pnl"] = pd.to_numeric(df["pnl"], errors="coerce").fillna(0.0)
    df["return_pct"] = pd.to_numeric(df["return_pct"], errors="coerce").fillna(0.0)

    total_trades = len(df)
    winning_rate = float((df["pnl"] > 0).mean())

    gross_profit = df.loc[df["pnl"] > 0, "pnl"].sum()
    gross_loss = abs(df.loc[df["pnl"] < 0, "pnl"].sum())
    profit_factor = float(gross_profit / gross_loss) if gross_loss > 0 else float("inf")

    average_trade_return = float(df["return_pct"].mean())
    cumulative_return = float((1 + df["return_pct"]).prod() - 1)

    equity_curve = (1 + df["return_pct"]).cumprod()
    running_max = equity_curve.cummax()
    drawdown = (running_max - equity_curve) / running_max
    max_drawdown = float(drawdown.max()) if len(drawdown) > 0 else 0.0

    std = float(df["return_pct"].std(ddof=1)) if total_trades > 1 else 0.0
    sharpe_ratio = float(df["return_pct"].mean() / std) if std > 0 else 0.0

    metrics = pd.DataFrame(
        [
            {
                "total_trades": total_trades,
                "winning_rate": winning_rate,
                "profit_factor": profit_factor,
                "average_trade_return": average_trade_return,
                "cumulative_return": cumulative_return,
                "max_drawdown": max_drawdown,
                "sharpe_ratio": sharpe_ratio,
            }
        ]
    )

    return metrics


def save_metrics(metrics_df: pd.DataFrame, ticker: str, strategy_name: str) -> Path:
    output_dir = Path("data/processed/metrics")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{ticker}_{strategy_name}_metrics.csv"
    metrics_df.to_csv(output_path, index=False)

    print(f"Saved metrics to {output_path}")
    return output_path