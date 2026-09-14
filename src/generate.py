from groq import Groq
from src.config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")

NEWSLETTER_SYSTEM = """You are a tech news curator for venture capital partner.
Given a list of scored news articles, write a short newsletter intro and format the top 10 as bullet points.

Rules:
- Intro: 2-3 sentences, hooky, no fluff. Focus on "what this means for Ventures".
- Each bullet: headline + one-line why-it-matters (max 20 words).
- Tone: sharp, human, slightly opinionated.
- Output valid HTML (simple <p> and <ul><li>).
- Return ONLY the HTML body. No markdown, no code fences."""
def generate_newsletter(articles):
    # articles = list of (aid, score, title, summary, source, url, reason)
    lines = []
    for i, (aid, score, title, summary, source, url, reason) in enumerate(articles, 1):
        lines.append(f"{i}. [{score}] {title}\n   Source: {source}\n   Why: {reason}\n   URL: {url}")

    user_msg = "Here are the candidate articles:\n\n" + "\n\n".join(lines) + "\n\nWrite the newsletter."

    try:
        resp = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": NEWSLETTER_SYSTEM},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.7,
            max_tokens=1200,
            reasoning_effort="low",
        )
        raw = resp.choices[0].message.content
        if not raw:
            return None
        return raw.strip()
    except Exception as e:
        print(f"[newsletter fail] {type(e).__name__}: {e}")
        return None