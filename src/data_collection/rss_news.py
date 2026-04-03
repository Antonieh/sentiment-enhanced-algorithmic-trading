from pathlib import Path
import json
from datetime import datetime, timezone

import feedparser


def fetch_rss_news(ticker: str, limit: int = 20) -> Path:
    output_dir = Path("data/raw/rss_news") / ticker
    output_dir.mkdir(parents=True, exist_ok=True)

    rss_url = f"https://finance.yahoo.com/rss/headline?s={ticker}"
    feed = feedparser.parse(rss_url)

    if not feed.entries:
        raise ValueError(f"No RSS news entries returned for {ticker}")

    collected_at = datetime.now(timezone.utc)
    snapshot_date = collected_at.strftime("%Y-%m-%d")
    snapshot_time = collected_at.strftime("%H%M%S")

    news_items = []
    for entry in feed.entries[:limit]:
        news_items.append(
            {
                "ticker": ticker,
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "published_parsed": list(entry.published_parsed) if entry.get("published_parsed") else None,
                "collected_at": collected_at.isoformat(),
                "source": "Yahoo Finance RSS",
            }
        )

    output_path = output_dir / f"{ticker}_{snapshot_date}_{snapshot_time}_rss_news.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(news_items, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(news_items)} RSS news entries for {ticker} to {output_path}")
    return output_path