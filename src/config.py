import os
from dotenv import load_dotenv
import re

def sanitize_key(raw):
    if not raw:
        return raw
    cleaned = re.sub(r"[^\x21-\x7E]", "", raw)  # keep printable ASCII only
    return cleaned

GROQ_API_KEY = sanitize_key(os.getenv("GROQ_API_KEY"))

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print(f"[debug] key_len={len(GROQ_API_KEY) if GROQ_API_KEY else 0}")

DB_PATH = "data/news.db"

RSS_FEEDS = {
    # Tier 1 — insider chatter + analysis
    "Techmeme": "https://www.techmeme.com/feed.xml",
    "Stratechery": "https://stratechery.com/feed/",
    "Platformer": "https://www.platformer.news/feed",
    "Import AI": "https://importai.substack.com/feed",
    "The Rundown AI": "https://www.therundown.ai/feed",

    # Tier 2 — mainstream AI/tech desks
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "The Verge AI": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "Ars Technica": "https://arstechnica.com/feed/",
    "Wired": "https://www.wired.com/feed/rss",
    "MIT Tech Review AI": "https://www.technologyreview.com/topic/artificial-intelligence/feed/",

    # Tier 3 — aggregators
    "Hacker News": "https://hnrss.org/frontpage",
    "Axios Tech": "https://api.axios.com/feed/technology",
}
GROQ_MODEL = "openai/gpt-oss-120b"
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")