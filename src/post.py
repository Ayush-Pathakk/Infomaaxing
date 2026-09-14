import tweepy
from src.config import X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET

def get_client():
    return tweepy.Client(
        consumer_key=X_API_KEY,
        consumer_secret=X_API_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_SECRET,
    )

def post_tweet(text):
    try:
        client = get_client()
        resp = client.create_tweet(text=text, user_auth=True)
        tweet_id = resp.data["id"]
        print(f"[posted] https://x.com/i/status/{tweet_id}")
        return tweet_id
    except Exception as e:
        print(f"[post fail] {type(e).__name__}: {e}")
        return None
def verify_auth():
    client = get_client()
    try:
        me = client.get_me(user_auth=True)
        print(f"[auth ok] @{me.data.username}")
        return True
    except Exception as e:
        print(f"[auth fail] {type(e).__name__}: {e}")
        return False