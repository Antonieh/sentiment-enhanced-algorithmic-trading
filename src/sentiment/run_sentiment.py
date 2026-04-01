from pathlib import Path
import json

import pandas as pd

from src.sentiment.finbert_model import load_finbert_pipeline
from src.sentiment.scoring import (
    scores_to_dict,
    article_sentiment_score,
    article_confidence,
)


def score_rss_news_file(ticker: str) -> Path:
    input_path = Path("data/raw/rss_news") / f"{ticker}_rss_news.json"
    output_dir = Path("data/processed/sentiment")
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Missing RSS news file: {input_path}")

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
            }
        )

    scored_df = pd.DataFrame(scored_rows)

    output_path = output_dir / f"{ticker}_article_sentiment.csv"
    scored_df.to_csv(output_path, index=False)

    print(f"Saved article-level sentiment for {ticker} to {output_path}")
    return output_path