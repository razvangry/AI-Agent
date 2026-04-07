# rss_news.py
import feedparser
import pandas as pd
from datetime import datetime
import os

# -------------------------
# LISTA EXTINSA DE RSS FEEDS
# -------------------------
RSS_FEEDS = {
    # Tech
    "TechCrunch": "http://feeds.feedburner.com/TechCrunch/",
    "Ars Technica": "http://feeds.arstechnica.com/arstechnica/index",
    "The Verge": "https://www.theverge.com/rss/index.xml",

    # General News
    "BBC World": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "BBC Technology": "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "Reuters World": "https://www.reutersagency.com/feed/?best-topics=world&post_type=best",

    # Business
    "Bloomberg": "https://feeds.bloomberg.com/markets/news.rss",
    "Financial Times": "https://www.ft.com/rss/home",

    # Sports
    "ESPN NBA": "https://www.espn.com/espn/rss/nba/news",
    "Sky Sports": "https://www.skysports.com/rss/12040",

    # AI / Tech
    "MIT Tech Review": "https://www.technologyreview.com/feed/",
    "Wired": "https://www.wired.com/feed/rss",

    # Gaming
    "PC Gamer": "https://www.pcgamer.com/rss/",
    "IGN": "https://feeds.feedburner.com/ign/all"
}

MAX_ARTICLES_PER_FEED = 5
OUTPUT_FILE = "rss_news_report.csv"

# -------------------------
# FUNCTIE PARSARE RSS
# -------------------------
def parse_rss_feed(feed_url, source_name, run_date):
    parsed_feed = feedparser.parse(feed_url)
    articles = []

    for entry in parsed_feed.entries[:MAX_ARTICLES_PER_FEED]:
        articles.append({
            "source": source_name,
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "collected_date": run_date
        })

    return articles

# -------------------------
# MAIN
# -------------------------
def main():
    all_articles = []

    run_date = datetime.now().strftime("%Y-%m-%d")

    for source_name, feed_url in RSS_FEEDS.items():
        print(f"Colectez articole de la: {source_name}")
        try:
            articles = parse_rss_feed(feed_url, source_name, run_date)
            all_articles.extend(articles)
        except Exception as e:
            print(f"Eroare la {source_name}: {e}")

    new_df = pd.DataFrame(all_articles)

    # Dacă există deja CSV → append
    if os.path.exists(OUTPUT_FILE):
        old_df = pd.read_csv(OUTPUT_FILE)
        combined_df = pd.concat([old_df, new_df], ignore_index=True)
    else:
        combined_df = new_df

    combined_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Raport actualizat în {OUTPUT_FILE}")

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    main()