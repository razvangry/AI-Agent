# rss_news_telegram_mobile.py
import csv
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
# INCARCARE CSV
# -------------------------
def load_csv(filename):
    data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

# -------------------------
# CONSTRUIRE MESAJ
# -------------------------
def build_summary_message(data):
    total_articles = len(data)
    pos = sum(1 for d in data if d["sentiment"] == "positive")
    neg = sum(1 for d in data if d["sentiment"] == "negative")
    neu = sum(1 for d in data if d["sentiment"] == "neutral")

    message = "📊 RSS NEWS SUMMARY\n\n"
    message += f"🌍 TOTAL: {total_articles} articole\n"
    message += f"👍 {pos} ({pos/total_articles:.1%})\n"
    message += f"👎 {neg} ({neg/total_articles:.1%})\n"
    message += f"😐 {neu} ({neu/total_articles:.1%})\n\n"

    # Grupare pe surse
    sources = list({d["source"] for d in data})

    for source in sources:
        message += f"📰 {source}\n"
        source_articles = [d for d in data if d["source"] == source][:5]  # top 5 per source

        for row in source_articles:
            icon = {"positive":"🟢", "negative":"🔴", "neutral":"🟡"}.get(row["sentiment"], "⚪")
            message += f"{icon} {row['title']}\n"
            message += f"🔗 {row['link']}\n"

        message += "\n"

    return message

# -------------------------
# SPLIT MESAJ
# -------------------------
def split_message(text, max_length=MAX_MESSAGE_LENGTH):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

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
    data = load_csv(INPUT_FILE)

    print("Generez mesaj...")
    message = build_summary_message(data)

    print("Trimit pe Telegram...")
    send_telegram_message(message)

    print("Gata!")

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    main()