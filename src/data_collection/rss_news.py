from pathlib import Path
import json

import feedparser


def fetch_rss_news(ticker: str) -> None:
    output_dir = Path("data/raw/news")
    output_dir.mkdir(parents=True, exist_ok=True)

    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    feed = feedparser.parse(url)

    entries = []
    for entry in feed.entries:
        entries.append(
            {
                "ticker": ticker,
                "title": getattr(entry, "title", ""),
                "summary": getattr(entry, "summary", ""),
                "link": getattr(entry, "link", ""),
                "published": getattr(entry, "published", ""),
            }
        )

    output_path = output_dir / f"{ticker}_news.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(entries)} news entries for {ticker} to {output_path}")