from pathlib import Path
import pandas as pd


def aggregate_daily_sentiment(ticker: str) -> None:
    input_path = Path("data/processed/sentiment") / f"{ticker}_article_sentiment.csv"
    output_dir = Path("data/processed/sentiment")
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Missing article sentiment file: {input_path}")

    df = pd.read_csv(input_path)

    if df.empty:
        raise ValueError(f"No article sentiment data found for {ticker}")

    # Convert published timestamp to date
    df["published"] = pd.to_datetime(df["published"], errors="coerce")
    df = df.dropna(subset=["published"])
    df["date"] = df["published"].dt.date

    # Confidence weight: max of class probabilities
    df["confidence_weight"] = df[["p_positive", "p_neutral", "p_negative"]].max(axis=1)

    # Weighted numerator
    df["weighted_score"] = df["confidence_weight"] * df["article_sentiment_score"]

    grouped = df.groupby("date").agg(
        n_articles=("article_sentiment_score", "count"),
        weighted_score_sum=("weighted_score", "sum"),
        confidence_weight_sum=("confidence_weight", "sum"),
        mean_article_score=("article_sentiment_score", "mean"),
    ).reset_index()

    grouped["S_t"] = grouped["weighted_score_sum"] / grouped["confidence_weight_sum"]
    grouped["M_t"] = grouped["S_t"].abs()
    grouped["ticker"] = ticker

    output_path = output_dir / f"{ticker}_daily_sentiment.csv"
    grouped.to_csv(output_path, index=False)

    print(f"Saved daily sentiment for {ticker} to {output_path}")