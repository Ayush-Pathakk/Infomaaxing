from src.db import init_db, save_posted
from src.fetch import fetch_all
from src.filter import pick_top_articles
from src.generate import generate_newsletter
from src.mailer import send_newsletter
import sys

def main():
    conn = init_db()
    fetch_all(conn)

    print("\n--- Scoring articles ---")
    articles = pick_top_articles(conn)

    if not articles:
        print("No articles scored >= 7 today. Exiting with error so workflow fails visibly.")
        conn.close()
        sys.exit(1)

    print(f"\n>>> Selected {len(articles)} articles for newsletter")

    print("\n--- Generating newsletter ---")
    html = generate_newsletter(articles)

    if not html:
        print("Newsletter generation failed.")
        conn.close()
        return

    print(f"Newsletter HTML length: {len(html)} chars")


    print("\n--- Sending email ---")
    if len(articles) < 5:
        print(f"Only {len(articles)} articles. Skipping send.")
        conn.close()
        return
        
    if send_newsletter(html):
        # Mark all selected articles as posted
        for aid, score, title, summary, source, url, reason in articles:
            save_posted(conn, aid, f"[newsletter] {title}", "email")
        print("Done. DB updated.")
    else:
        print("Send failed. DB not updated.")

    conn.close()

if __name__ == "__main__":
    main()