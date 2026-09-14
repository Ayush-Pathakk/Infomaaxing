import streamlit as st
import sqlite3
import os
from datetime import datetime

st.set_page_config(page_title="AI News Agent", page_icon="📰", layout="wide")

st.title("📰 AI/Tech News Agent")
st.caption("Autonomous agent that curates daily student-relevant AI/tech news")

DB = "data/news.db"

def load_data():
    if not os.path.exists(DB):
        return [], []
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        SELECT title, source, url, fetched_at
        FROM articles
        ORDER BY fetched_at DESC
        LIMIT 20
    """)
    fetched = c.fetchall()

    c.execute("""
        SELECT a.title, a.source, a.url, p.tweet_text, p.posted_at
        FROM posted p
        JOIN articles a ON a.id = p.article_id
        ORDER BY p.posted_at DESC
        LIMIT 10
    """)
    sent = c.fetchall()
    conn.close()
    return fetched, sent

fetched, sent = load_data()

col1, col2, col3 = st.columns(3)
col1.metric("Articles fetched", len(fetched))
col2.metric("Newsletters sent", len(sent))
col3.metric("Last run", datetime.now().strftime("%b %d, %H:%M"))

st.divider()

st.subheader("📬 Latest newsletters sent")
if not sent:
    st.info("No newsletters yet. Run `python main.py` locally or trigger the workflow.")
else:
    for title, source, url, body, posted_at in sent:
        with st.expander(f"**{title[:80]}** — {source}"):
            st.write(body[:500])
            st.markdown(f"[Read original]({url})")
            st.caption(f"Sent: {posted_at}")

st.divider()

st.subheader("🗞️ Recently fetched articles")
if not fetched:
    st.info("No articles in DB. Run `python main.py` first.")
else:
    for title, source, url, fetched_at in fetched[:10]:
        st.markdown(f"- **{title[:100]}** — *{source}* · [link]({url})")

st.divider()
st.caption("Built with Python · Groq · SQLite · GitHub Actions")