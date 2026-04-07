# rss_news_telegram.py
import pandas as pd
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -------------------------
# CONFIG
# -------------------------
INPUT_FILE = "rss_news_with_sentiment.csv"

BOT_TOKEN = "8487868674:AAH8IQvrEsXCSK3I2ZHwphPWnKo3GA4KAZo"
CHAT_ID = "8760146912"

MAX_MESSAGE_LENGTH = 4000  # Telegram limit ~4096

# -------------------------
# GENERARE MESAJ
# -------------------------
def build_summary_message(df):
    total_articles = len(df)
    sentiment_counts = df["sentiment"].value_counts()

    pos = sentiment_counts.get("positive", 0)
    neg = sentiment_counts.get("negative", 0)
    neu = sentiment_counts.get("neutral", 0)

    message = "📊 RSS NEWS SUMMARY\n\n"

    # TOTAL
    message += "🌍 TOTAL\n"
    message += f"📰 {total_articles} articole\n"

    if total_articles > 0:
        message += f"👍 {pos} ({pos/total_articles:.1%})\n"
        message += f"👎 {neg} ({neg/total_articles:.1%})\n"
        message += f"😐 {neu} ({neu/total_articles:.1%})\n\n"

    # PE SURSE
    sources = df["source"].unique()

    for source in sources:
        source_df = df[df["source"] == source].head(5)

        message += f"📰 {source}\n"

        for _, row in source_df.iterrows():
            icon = {
                "positive": "🟢",
                "negative": "🔴",
                "neutral": "🟡"
            }.get(row["sentiment"], "⚪")

            message += f"{icon} {row['title']}\n"
            message += f"🔗 {row['link']}\n"

        message += "\n"

    return message

# -------------------------
# SPLIT MESAJ
# -------------------------
def split_message(text, max_length=MAX_MESSAGE_LENGTH):
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

# -------------------------
# TRIMITERE TELEGRAM
# -------------------------
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    messages = split_message(text)

    for msg in messages:
        payload = {
            "chat_id": CHAT_ID,
            "text": msg,
            "disable_web_page_preview": True
        }

        response = requests.post(url, data=payload, verify=False)
        print(response.json())

# -------------------------
# MAIN
# -------------------------
def main():
    print("Încarc CSV...")
    df = pd.read_csv(INPUT_FILE)

    print("Generez mesaj...")
    message = build_summary_message(df)

    print("Trimit pe Telegram...")
    send_telegram_message(message)

    print("Gata!")

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    main()