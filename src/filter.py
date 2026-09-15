import json
from groq import Groq
from src.config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are a news analyst for students (undergrad + grad).
Given a news headline + summary, decide how much it affects students' careers, education, finances, or future.

Score 1-10:
- 9-10: Directly changes student life (AI job market shifts, visa rules, exam policy, tuition, layoffs in tech)
- 7-8: Strongly relevant (new AI tools that reshape skills, big tech hiring trends, education funding)
- 4-6: Tangentially relevant (general tech news with weak student angle)
- 1-3: Not relevant to students

Return ONLY valid JSON: {"score": <int>, "reason": "<10 words max>"}"""

STUDENT_KEYWORDS = [
    "student", "university", "college", "job", "hiring", "layoff",
    "internship", "visa", "loan", "exam", "scholarship", "placement",
    "ai", "artificial intelligence", "career", "degree", "campus",
    "graduate", "salary", "skill", "education", "research"
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
            WHERE posted_at >= datetime('now', '-1 day')
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
    return scored[:top_n]

import json
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