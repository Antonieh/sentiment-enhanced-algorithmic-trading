from pathlib import Path
import pandas as pd


def assign_strength_bin(m_t: float) -> str:
    if m_t == 0:
        return "0"
    elif m_t <= 0.2:
        return "(0,0.2]"
    elif m_t <= 0.4:
        return "(0.2,0.4]"
    elif m_t <= 0.6:
        return "(0.4,0.6]"
    elif m_t <= 0.8:
        return "(0.6,0.8]"
    else:
        return "(0.8,1.0]"


def analyze_signal_strength(trades_df: pd.DataFrame) -> pd.DataFrame:
    if trades_df.empty:
        return pd.DataFrame(
            columns=[
                "strength_bin",
                "n_trades",
                "winning_rate",
                "average_pnl",
                "profit_factor",
            ]
        )

    df = trades_df.copy()
    df["M_t_entry"] = pd.to_numeric(df["M_t_entry"], errors="coerce").fillna(0.0)
    df["pnl"] = pd.to_numeric(df["pnl"], errors="coerce").fillna(0.0)

    df["strength_bin"] = df["M_t_entry"].apply(assign_strength_bin)

    rows = []
    for strength_bin, group in df.groupby("strength_bin"):
        n_trades = len(group)
        winning_rate = float((group["pnl"] > 0).mean()) if n_trades > 0 else 0.0
        average_pnl = float(group["pnl"].mean()) if n_trades > 0 else 0.0

        gross_profit = group.loc[group["pnl"] > 0, "pnl"].sum()
        gross_loss = abs(group.loc[group["pnl"] < 0, "pnl"].sum())
        profit_factor = float(gross_profit / gross_loss) if gross_loss > 0 else float("inf")

        rows.append(
            {
                "strength_bin": strength_bin,
                "n_trades": n_trades,
                "winning_rate": winning_rate,
                "average_pnl": average_pnl,
                "profit_factor": profit_factor,
            }
        )

    result = pd.DataFrame(rows).sort_values("strength_bin").reset_index(drop=True)
    return result


def save_signal_strength_analysis(result_df: pd.DataFrame, ticker: str, strategy_name: str) -> Path:
    output_dir = Path("data/processed/metrics")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{ticker}_{strategy_name}_signal_strength.csv"
    result_df.to_csv(output_path, index=False)

    print(f"Saved signal strength analysis to {output_path}")
    return output_path