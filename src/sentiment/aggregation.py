from pathlib import Path

import pandas as pd


def aggregate_daily_sentiment(ticker: str) -> Path:
    input_dir = Path("data/processed/sentiment") / ticker
    output_dir = Path("data/processed/sentiment")
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_dir.exists():
        raise FileNotFoundError(f"Missing sentiment directory: {input_dir}")

    files = sorted(input_dir.glob(f"{ticker}_*_article_sentiment.csv"))
    if not files:
        raise FileNotFoundError(f"No article sentiment files found for {ticker} in {input_dir}")

    frames = [pd.read_csv(path) for path in files]
    df = pd.concat(frames, ignore_index=True)

    required_cols = [
        "published",
        "title",
        "link",
        "p_positive",
        "p_negative",
        "p_neutral",
        "article_sentiment_score",
        "confidence",
    ]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for aggregation: {missing}")

    df["published"] = pd.to_datetime(df["published"], errors="coerce")
    df = df.dropna(subset=["published"]).copy()

    # Deduplicate repeated RSS items across snapshots
    df["title"] = df["title"].fillna("").astype(str)
    df["link"] = df["link"].fillna("").astype(str)
    df = df.drop_duplicates(subset=["published", "title", "link"]).copy()

    df["date"] = df["published"].dt.date

    if df.empty:
        daily_df = pd.DataFrame(columns=["date", "S_t", "M_t", "n_articles"])
    else:
        grouped = df.groupby("date", as_index=False).apply(
            lambda g: pd.Series(
                {
                    "S_t": (
                        (g["confidence"] * g["article_sentiment_score"]).sum()
                        / g["confidence"].sum()
                    )
                    if g["confidence"].sum() > 0
                    else 0.0,
                    "M_t": abs(
                        (
                            (g["confidence"] * g["article_sentiment_score"]).sum()
                            / g["confidence"].sum()
                        )
                        if g["confidence"].sum() > 0
                        else 0.0
                    ),
                    "n_articles": len(g),
                }
            )
        ).reset_index(drop=True)

        daily_df = grouped.sort_values("date").reset_index(drop=True)

    output_path = output_dir / f"{ticker}_daily_sentiment.csv"
    daily_df.to_csv(output_path, index=False)

    print(f"Saved daily sentiment for {ticker} to {output_path}")
    return output_path