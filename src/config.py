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

DB_PATH = "data/news.db"

RSS_FEEDS = {
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "The Verge AI": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
    "Ars Technica": "https://arstechnica.com/feed/",
    "MIT Tech Review AI": "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
    "Wired": "https://www.wired.com/feed/rss",
    "Economist Sci/Tech": "https://www.economist.com/science-and-technology/rss.xml",
    "BBC Tech": "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "BBC Education": "https://feeds.bbci.co.uk/news/education/rss.xml",
    "Guardian Tech": "https://feeds.theguardian.com/theguardian/technology/rss",
    "Guardian Education": "https://feeds.theguardian.com/theguardian/education/rss",
    "Hacker News": "https://hnrss.org/frontpage",
    "TOI Tech": "https://timesofindia.indiatimes.com/rssfeeds/66949542.cms",
}

GROQ_MODEL = "openai/gpt-oss-120b"
print(f"[debug] key_len={len(GROQ_API_KEY) if GROQ_API_KEY else 0}")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")