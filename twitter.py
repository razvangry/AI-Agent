# twitter_free_certifi.py
import tweepy
from textblob import TextBlob
import pandas as pd
import certifi
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl

# -------------------------
# CONFIG: Bearer Token
# -------------------------
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAAjj8gEAAAAAQCpGCkOCgRORAYLhCXgSOpAugh8%3DpKCkVK2Z4SPbWhYwjd8J07qtbTzepWVg48ZYg7ycraE9yOT5bD"

# -------------------------
# CONTURI PUBLICE
# -------------------------
PUBLIC_ACCOUNTS = ["nasa", "NBA", "PythonHub", "TechCrunch", "ESPN"]
MAX_TWEETS = 10

# -------------------------
# FORȚĂ SSL CERTIFI
# -------------------------
class SSLAdapter(HTTPAdapter):
    """Folosește certifi pentru Requests (rezolvă probleme SSL pe Windows)"""
    def __init__(self, **kwargs):
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ssl_context,
            **pool_kwargs
        )

# Crează session custom pentru Tweepy
session = requests.Session()
session.mount("https://", SSLAdapter())

# -------------------------
# CLIENT TWEEPY
# -------------------------
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# -------------------------
# FUNCTII UTILE
# -------------------------
def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity < 0:
        return "negative"
    else:
        return "neutral"

def collect_tweets_from_user(username, max_tweets=MAX_TWEETS):
    tweets_data = []
    try:
        # Obține user id
        user = client.get_user(username=username)
        if user.data:
            user_id = user.data.id
            # Colectează ultimele tweet-uri
            tweets = client.get_users_tweets(id=user_id, max_results=max_tweets)
            if tweets.data:
                for tweet in tweets.data:
                    sentiment = analyze_sentiment(tweet.text)
                    tweets_data.append({
                        "username": username,
                        "text": tweet.text,
                        "sentiment": sentiment
                    })
    except Exception as e:
        print(f"Eroare la @{username}: {e}")
    return tweets_data

# -------------------------
# MAIN
# -------------------------
def main():
    all_data = []
    for account in PUBLIC_ACCOUNTS:
        print(f"Colectez tweets de la: @{account}")
        data = collect_tweets_from_user(account)
        all_data.extend(data)

    df = pd.DataFrame(all_data)
    df.to_csv("twitter_report_free_certifi.csv", index=False)
    print("Raport salvat în twitter_report_free_certifi.csv")

if __name__ == "__main__":
    main()