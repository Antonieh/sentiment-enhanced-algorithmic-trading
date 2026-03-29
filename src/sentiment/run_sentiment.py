from pathlib import Path
import json
import pandas as pd

from src.sentiment.finbert_model import load_finbert_pipeline
from src.sentiment.scoring import scores_to_dict, article_sentiment_score


def build_text(title: str, summary: str) -> str:
    title = title or ""
    summary = summary or ""
    text = f"{title}. {summary}".strip()
    return text


def run_finbert_for_ticker(ticker: str) -> None:
    input_path = Path("data/raw/news") / f"{ticker}_news.json"
    output_dir = Path("data/processed/sentiment")
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Missing raw news file: {input_path}")

    with open(input_path, "r", encoding="utf-8") as f:
        entries = json.load(f)

    sentiment_pipeline = load_finbert_pipeline()

    rows = []
    for entry in entries:
        title = entry.get("title", "")
        summary = entry.get("summary", "")
        published = entry.get("published", "")
        link = entry.get("link", "")

        text = build_text(title, summary)

        if not text.strip():
            continue

        model_output = sentiment_pipeline(text)[0]
        prob_dict = scores_to_dict(model_output)
        s_it = article_sentiment_score(prob_dict)

        rows.append(
            {
                "ticker": ticker,
                "published": published,
                "title": title,
                "summary": summary,
                "link": link,
                "text": text,
                "p_positive": prob_dict["positive"],
                "p_neutral": prob_dict["neutral"],
                "p_negative": prob_dict["negative"],
                "article_sentiment_score": s_it,
            }
        )

    df = pd.DataFrame(rows)
    output_path = output_dir / f"{ticker}_article_sentiment.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved article-level sentiment for {ticker} to {output_path}")