from pathlib import Path
import pandas as pd


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


def build_metrics_summary(strategy_name: str) -> pd.DataFrame:
    rows = []

    for ticker in TICKERS:
        path = Path("data/processed/metrics") / f"{ticker}_{strategy_name}_metrics.csv"
        if not path.exists():
            continue

        df = pd.read_csv(path)
        if df.empty:
            continue

        row = df.iloc[0].to_dict()
        row["ticker"] = ticker
        row["strategy"] = strategy_name
        rows.append(row)

    if not rows:
        return pd.DataFrame()

    summary_df = pd.DataFrame(rows)

    cols = ["ticker", "strategy"] + [c for c in summary_df.columns if c not in ["ticker", "strategy"]]
    summary_df = summary_df[cols]

    return summary_df


def save_metrics_summary(summary_df: pd.DataFrame, strategy_name: str) -> Path:
    output_dir = Path("data/processed/metrics")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{strategy_name}_summary.csv"
    summary_df.to_csv(output_path, index=False)

    print(f"Saved summary metrics to {output_path}")
    return output_path


def main() -> None:
    for strategy_name in ["baseline_sma", "sentiment_sma"]:
        summary_df = build_metrics_summary(strategy_name)
        if summary_df.empty:
            print(f"No summary data for {strategy_name}")
        else:
            print(summary_df)
            save_metrics_summary(summary_df, strategy_name)


if __name__ == "__main__":
    main()