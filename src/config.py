import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.getenv("X_ACCESS_SECRET")

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
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")