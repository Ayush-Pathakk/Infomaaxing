import sqlite3
from src.config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            title TEXT,
            summary TEXT,
            source TEXT,
            published TEXT,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS posted (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER,
            tweet_text TEXT,
            tweet_id TEXT,
            posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn

def url_exists(conn, url):
    c = conn.cursor()
    c.execute("SELECT 1 FROM articles WHERE url = ?", (url,))
    return c.fetchone() is not None

def insert_article(conn, url, title, summary, source, published):
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO articles (url, title, summary, source, published) VALUES (?, ?, ?, ?, ?)",
            (url, title, summary, source, published)
        )
        conn.commit()
        return c.lastrowid
    except sqlite3.IntegrityError:
        return None

def save_posted(conn, article_id, tweet_text, tweet_id):
    c = conn.cursor()
    c.execute(
        "INSERT INTO posted (article_id, tweet_text, tweet_id) VALUES (?, ?, ?)",
        (article_id, tweet_text, tweet_id)
    )
    conn.commit()