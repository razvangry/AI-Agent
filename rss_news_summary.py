# rss_news_summary.py
import pandas as pd

# -------------------------
# Load CSV
# -------------------------
df = pd.read_csv("rss_news_report.csv")

# -------------------------
# Grupare pe surse
# -------------------------
sources = df['source'].unique()

print("\n📄 SUMMARY RSS NEWS\n")
for src in sources:
    articles = df[df['source'] == src]
    print(f"📰 {src} ({len(articles)} articole):\n")
    for idx, row in articles.iterrows():
        print(f"  - {row['title']}")
        print(f"    🔗 {row['link']}")
    print("\n" + "-"*50 + "\n")