from pathlib import Path
import json

import pandas as pd

from src.sentiment.finbert_model import load_finbert_pipeline
from src.sentiment.scoring import (
    scores_to_dict,
    article_sentiment_score,
    article_confidence,
)


def get_latest_rss_news_file(ticker: str) -> Path:
    input_dir = Path("data/raw/rss_news") / ticker
    if not input_dir.exists():
        raise FileNotFoundError(f"Missing RSS news directory: {input_dir}")

    files = sorted(input_dir.glob(f"{ticker}_*_rss_news.json"))
    if not files:
        raise FileNotFoundError(f"No RSS snapshot files found for {ticker} in {input_dir}")

    return files[-1]


def score_rss_news_file(ticker: str) -> Path:
    input_path = get_latest_rss_news_file(ticker)

    output_dir = Path("data/processed/sentiment") / ticker
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(input_path, "r", encoding="utf-8") as f:
        news_items = json.load(f)

    sentiment_pipeline = load_finbert_pipeline()

    scored_rows = []
    for item in news_items:
        title = item.get("title", "")
        summary = item.get("summary", "")
        text = f"{title}. {summary}".strip()

        if not text:
            continue

        model_output = sentiment_pipeline(text)[0]
        prob_dict = scores_to_dict(model_output)

        scored_rows.append(
            {
                "ticker": ticker,
                "published": item.get("published", ""),
                "title": title,
                "summary": summary,
                "link": item.get("link", ""),
                "p_positive": prob_dict["p_positive"],
                "p_negative": prob_dict["p_negative"],
                "p_neutral": prob_dict["p_neutral"],
                "article_sentiment_score": article_sentiment_score(prob_dict),
                "confidence": article_confidence(prob_dict),
                "collected_at": item.get("collected_at", ""),
            }
        )

    scored_df = pd.DataFrame(scored_rows)

    stem = input_path.stem.replace("_rss_news", "_article_sentiment")
    output_path = output_dir / f"{stem}.csv"
    scored_df.to_csv(output_path, index=False)

    print(f"Saved article-level sentiment for {ticker} to {output_path}")
    return output_path