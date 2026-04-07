# rss_news_sentiment_summary.py
import pandas as pd

INPUT_FILE = "rss_news_with_sentiment.csv"

# -------------------------
# MAIN
# -------------------------
def main():
    print("\n📊 RSS NEWS SENTIMENT SUMMARY\n")

    df = pd.read_csv(INPUT_FILE)

    # -------------------------
    # 🔥 TOTAL GENERAL
    # -------------------------
    total_articles = len(df)
    sentiment_counts_total = df["sentiment"].value_counts()

    total_pos = sentiment_counts_total.get("positive", 0)
    total_neg = sentiment_counts_total.get("negative", 0)
    total_neu = sentiment_counts_total.get("neutral", 0)

    print("🌍 TOTAL GENERAL\n")
    print(f"📰 Total articole: {total_articles}")

    if total_articles > 0:
        print(f"👍 Pozitive: {total_pos} ({total_pos/total_articles:.1%})")
        print(f"👎 Negative: {total_neg} ({total_neg/total_articles:.1%})")
        print(f"😐 Neutre: {total_neu} ({total_neu/total_articles:.1%})")

    print("\n" + "="*60)

    # -------------------------
    # PE SURSE
    # -------------------------
    sources = df["source"].unique()

    for source in sources:
        source_df = df[df["source"] == source]

        print(f"\n📰 {source} ({len(source_df)} articole)\n")

        sentiment_counts = source_df["sentiment"].value_counts()

        pos = sentiment_counts.get("positive", 0)
        neg = sentiment_counts.get("negative", 0)
        neu = sentiment_counts.get("neutral", 0)

        print(f"   👍 Pozitive: {pos}")
        print(f"   👎 Negative: {neg}")
        print(f"   😐 Neutre: {neu}\n")

        for _, row in source_df.iterrows():
            sentiment_icon = {
                "positive": "🟢",
                "negative": "🔴",
                "neutral": "🟡"
            }.get(row["sentiment"], "⚪")

            print(f"{sentiment_icon} {row['title']}")
            print(f"   🔗 {row['link']}")
            print(f"   📅 {row.get('collected_date', '')}")
            print()

        print("-" * 60)

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    main()