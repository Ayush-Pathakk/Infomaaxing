import streamlit as st
import sqlite3
import os
import urllib.request
from datetime import datetime

st.set_page_config(
    page_title="AI News Agent",
    page_icon="📰",
    layout="wide",
)

# ---------- Styles ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(160deg, #0e1117 0%, #131a24 60%, #0e1117 100%);
        color: #e6edf3;
    }
    h1, h2, h3 { color: #e6edf3; letter-spacing: -0.02em; }
    .title-tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 999px;
        background: rgba(88, 166, 255, 0.12);
        color: #58a6ff;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.04em;
        margin-bottom: 10px;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.025);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 18px 20px;
        transition: 0.2s ease;
    }
    .metric-card:hover {
        border-color: rgba(88, 166, 255, 0.35);
        background: rgba(88, 166, 255, 0.04);
    }
    .metric-label {
        font-size: 12px;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .metric-value {
        font-size: 30px;
        font-weight: 700;
        color: #e6edf3;
        margin-top: 4px;
    }
    .news-item {
        padding: 14px 16px;
        border-left: 3px solid #58a6ff;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .news-item a { color: #58a6ff; text-decoration: none; font-weight: 600; }
    .news-item a:hover { text-decoration: underline; }
    .news-meta { font-size: 12px; color: #8b949e; margin-top: 4px; }
    hr { border-color: rgba(255,255,255,0.06); }
</style>
""", unsafe_allow_html=True)

# ---------- Config ----------
DB = "data/news.db"
GITHUB_RAW = "https://raw.githubusercontent.com/Ayush-Pathakk/Infomaaxing/main/data/news.db"

# ---------- Header ----------
st.markdown('<span class="title-tag">AUTONOMOUS · DAILY · AI/TECH</span>', unsafe_allow_html=True)
st.title("📰 AI News Agent")
st.caption("Curated daily digest of AI/tech news that actually matters.")

# ---------- Refresh button ----------
colA, colB = st.columns([7, 1])
with colB:
    if st.button("🔄 Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ---------- Data ----------
def fetch_latest_db():
    try:
        urllib.request.urlretrieve(GITHUB_RAW, DB)
    except Exception:
        pass  # fall back to cached DB

@st.cache_data(ttl=60)
def load_data():
    fetch_latest_db()
    if not os.path.exists(DB):
        return [], []
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT title, source, url, fetched_at FROM articles
        ORDER BY fetched_at DESC LIMIT 30
    """)
    fetched = c.fetchall()
    c.execute("""
        SELECT a.title, a.source, a.url, p.tweet_text, p.posted_at
        FROM posted p JOIN articles a ON a.id = p.article_id
        ORDER BY p.posted_at DESC LIMIT 10
    """)
    sent = c.fetchall()
    conn.close()
    return fetched, sent

fetched, sent = load_data()

# ---------- Metrics ----------
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Articles fetched</div>
        <div class="metric-value">{len(fetched)}</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Newsletters sent</div>
        <div class="metric-value">{len(sent)}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------- Latest newsletter ----------
st.subheader("📬 Latest newsletter")
if not sent:
    st.info("No newsletters yet.")
else:
    for title, source, url, body, posted_at in sent:
        with st.expander(f"**{title[:90]}** — {source}"):
            st.write(body[:600])
            st.markdown(f"[Read original →]({url})")
            st.caption(f"Sent: {posted_at}")

st.divider()

# ---------- Recently fetched ----------
st.subheader("🗞️ Recently fetched")
if not fetched:
    st.info("No articles in DB yet.")
else:
    for title, source, url, fetched_at in fetched[:10]:
        st.markdown(f"""
        <div class="news-item">
            <a href="{url}" target="_blank">{title[:120]}</a>
            <div class="news-meta">{source} · fetched {fetched_at}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.caption("Built with Python · Groq · SQLite · GitHub Actions")