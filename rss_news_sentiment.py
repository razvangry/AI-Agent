# rss_news_sentiment.py
import pandas as pd
from textblob import TextBlob

INPUT_FILE = "rss_news_report.csv"
OUTPUT_FILE = "rss_news_with_sentiment.csv"

# -------------------------
# FUNCTIE SENTIMENT
# -------------------------
def analyze_sentiment(text):
    analysis = TextBlob(str(text))
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        sentiment = "positive"
    elif polarity < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return sentiment, polarity

# -------------------------
# MAIN
# -------------------------
def main():
    print("Încarc datele din CSV...")
    df = pd.read_csv(INPUT_FILE)

    sentiments = []
    polarities = []

    print("Analizez sentimentul pentru fiecare știre...")
    for title in df["title"]:
        sentiment, polarity = analyze_sentiment(title)
        sentiments.append(sentiment)
        polarities.append(polarity)

    # Adaugă coloane noi
    df["sentiment"] = sentiments
    df["polarity"] = polarities

    # Salvare
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Rezultatul a fost salvat în {OUTPUT_FILE}")

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    main()