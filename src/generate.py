from groq import Groq
from src.config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)

NEWSLETTER_SYSTEM = """You are a tech insider curating a daily digest for people who follow AI/tech closely.

Rules:
- Intro: 2-3 sentences. What's the ONE thing everyone's talking about today. Punchy, insider tone.
- Then a bulleted list of the top 10 articles.
- Each bullet MUST be: <li><a href="URL">Headline</a> — one-line why-it-matters (max 20 words)</li>
- Use the EXACT URL provided. Do not shorten, modify, or invent URLs.
- Tone: smart friend texting you. Dry humor OK. No corporate speak.
- Output valid HTML only. No markdown, no code fences.

Return ONLY the HTML body."""
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