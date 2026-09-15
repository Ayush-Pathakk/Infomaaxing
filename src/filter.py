import json
from groq import Groq
from src.config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are a tech insider curating a daily digest for people who follow AI/tech closely.

Score 1-10 on how "TBPN-worthy" the article is:
- 9-10: Insider drama, founder beef, big-money moves ($100M+), policy fights, exec departures, bold public statements from Altman/Musk/Dario/etc.
- 7-8: Model releases, funding rounds, acquisitions, regulatory news, notable failures/outages, hot takes from respected VCs
- 5-6: Product updates, technical deep dives, general industry news
- 1-3: Listicles, tutorials, "top 10 AI tools", education policy, generic how-tos

Favor: specific names, specific numbers, conflict, novelty, timeliness, Big updates , new fameworks ,big Industry change.
Penalize: vague, evergreen, promotional, clickbait.

Return ONLY valid JSON: {"score": <int>, "reason": "<10 words max>"}"""

STUDENT_KEYWORDS = [
    # People
    "altman", "musk", "amodei", "huang", "sacks", "nadella", "pichai",
    "zuckerberg", "hassabis", "sutskever", "karpathy",
    # Companies
    "openai", "anthropic", "nvidia", "google", "microsoft", "meta",
    "xai", "tesla", "apple", "amazon", "deepmind",
    # Money moves
    "billion", "acquisition", "acquires", "funding", "raise", "ipo",
    "valuation", "series",
    # Drama/action
    "lawsuit", "sues", "resigns", "fired", "departs", "layoff",
    "regulation", "ban", "investigation", "antitrust",
    # Products
    "gpt", "gemini", "claude", "llama", "grok", "model", "release",
    "launch", "unveil",
]

SKIP_SOURCES = {"TOI Tech", "Hacker News"}

def keyword_gate(title, summary):
    text = (title + " " + summary).lower()
    return any(k in text for k in STUDENT_KEYWORDS)

def score_article(title, summary):
    user_msg = f"Title: {title}\nSummary: {summary[:400]}"
    try:
        resp = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        data = json.loads(resp.choices[0].message.content)
        return int(data.get("score", 0)), data.get("reason", "")
    except Exception as e:
        print(f"[score fail] {type(e).__name__}: {e}")
        return 0, "error"

def pick_top_articles(conn, min_score=6, batch_limit=25, top_n=10):
    c = conn.cursor()
    c.execute("""
        SELECT id, title, summary, source, url FROM articles
        WHERE id NOT IN (
            SELECT article_id FROM posted
            WHERE posted_at >= datetime('now', '-3 days')
        )
        ORDER BY fetched_at DESC
        LIMIT 100
    """)
    rows = c.fetchall()

    scored = []
    count = 0
    for aid, title, summary, source, url in rows:
        if source in SKIP_SOURCES:
            continue
        if not keyword_gate(title, summary):
            continue
        if count >= batch_limit:
            break

        score, reason = score_article(title, summary)
        count += 1
        print(f"[{score:>2}] {source}: {title[:70]}")

        if score >= min_score:
            scored.append((aid, score, title, summary, source, url, reason))

    scored.sort(key=lambda x: x[1], reverse=True)
    top = [a for a in scored if a[1] >= min_score][:top_n]

    # Backfill if we don't have 10
    if len(top) < top_n:
        extra = [a for a in scored if a[1] >= 4 and a not in top]
        top += extra[:top_n - len(top)]

    return top[:top_n]

import time
from groq import Groq
from src.config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)

# ... SYSTEM_PROMPT, STUDENT_KEYWORDS, SKIP_SOURCES unchanged ...

def keyword_gate(title, summary):
    text = (title + " " + summary).lower()
    return any(k in text for k in STUDENT_KEYWORDS)

def score_article(title, summary, retries=3):
    user_msg = f"Title: {title}\nSummary: {summary[:400]}"
    for attempt in range(retries):
        try:
            resp = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.2,
                response_format={"type": "json_object"},
            )
            data = json.loads(resp.choices[0].message.content)
            return int(data.get("score", 0)), data.get("reason", "")
        except Exception as e:
            if attempt < retries - 1:
                wait = 2 ** attempt  # 1s, 2s, 4s
                print(f"[retry {attempt+1}] {type(e).__name__}, waiting {wait}s")
                time.sleep(wait)
            else:
                print(f"[score fail] {type(e).__name__}: {e}")
                return 0, "error"