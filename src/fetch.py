import feedparser
from src.config import RSS_FEEDS
from src.db import url_exists, insert_article

def fetch_all(conn):
    new_count = 0
    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:15]:
                link = entry.get("link", "")
                title = entry.get("title", "").strip()
                summary = entry.get("summary", "")[:500]
                published = entry.get("published", "")

                if not link or not title:
                    continue
                if url_exists(conn, link):
                    continue

                insert_article(conn, link, title, summary, source, published)
                new_count += 1

            print(f"[OK] {source}: {len(feed.entries)} entries")
        except Exception as e:
            print(f"[FAIL] {source}: {e}")

    print(f"\nTotal new articles: {new_count}")
    conn.execute("DELETE FROM articles WHERE fetched_at < datetime('now', '-2 days')")
    conn.commit()
    return new_count