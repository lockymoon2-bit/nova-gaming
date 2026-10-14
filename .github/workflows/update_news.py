import json
import time
import feedparser
from datetime import datetime, timezone

FEEDS = [
("Zoomg", "https://www.zoomg.ir/feed/"),
("Gamefa", "https://gamefa.com/feed/"),
]

def clean_text(value):
return " ".join(str(value or "").split())

def main():
news = []
seen = set()

for source, url in FEEDS:
    try:
        feed = feedparser.parse(url)

        if getattr(feed, "bozo", False) and not feed.entries:
            print(f"Feed unavailable: {source}")
            continue

        for entry in feed.entries[:20]:
            title = clean_text(entry.get("title"))
            link = clean_text(entry.get("link"))

            if not title or not link or link in seen:
                continue

            seen.add(link)

            summary = clean_text(
                entry.get("summary", entry.get("description", ""))
            )

            news.append({
                "title": title,
                "link": link,
                "summary": summary[:500],
                "source": source,
                "published": clean_text(
                    entry.get("published", entry.get("updated", ""))
                )
            })

    except Exception as error:
        print(f"Error reading {source}: {error}")

news.sort(key=lambda item: item["published"], reverse=True)

output = {
    "updated": datetime.now(timezone.utc).isoformat(),
    "articles": news[:40]
}

with open("news.json", "w", encoding="utf-8") as file:
    json.dump(output, file, ensure_ascii=False, indent=2)

print(f"Saved {len(news[:40])} news articles.")

if name == "main":
main()
