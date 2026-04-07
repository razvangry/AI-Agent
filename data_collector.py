import requests
import json
import os
import certifi
from config import API_KEY_ODDS, SPORTS

# Path pentru cache
CACHE_FILE = "odds_cache.json"

# Config fix
REGIONS = "eu"      # Europa
MARKETS = "h2h"     # 1X2 / moneyline
ODDS_API_URL = "https://api.the-odds-api.com/v4/sports/{sport}/odds/"

def _load_cache():
    """Încarcă odds din fișier cache"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("❌ ERROR loading cache:", e)
            return []
    return []

def _save_cache(data):
    """Salvează odds în cache"""
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print("❌ ERROR saving cache:", e)

def get_odds():
    """Colectează odds pentru toate sporturile din config"""
    all_matches = []

    for sport in SPORTS:
        try:
            url = ODDS_API_URL.format(sport=sport)
            params = {
                "apiKey": API_KEY_ODDS,
                "regions": REGIONS,
                "markets": MARKETS
            }

            print(f"\n➡️ Fetching: {sport}")

            # Folosim certifi pentru SSL fix
            response = requests.get(url, params=params, timeout=10, verify=False)

            print(f"Status: {response.status_code}")
            print(f"Response (first 200 chars): {response.text[:200]}")

            response.raise_for_status()
            data = response.json()

            print(f"Events received: {len(data)}")

            # Parsează fiecare meci
            for event in data:
                home = event.get("home_team")
                away = event.get("away_team")
                if not home or not away:
                    continue

                match_name = f"{home} vs {away}"
                bookmakers = []

                for book in event.get("bookmakers", []):
                    if book.get("markets"):
                        h2h_market = next((m for m in book["markets"] if m["key"] == "h2h"), None)
                        if h2h_market and len(h2h_market.get("outcomes", [])) > 0:
                            # luam prima opțiune (home win) ca exemplu
                            outcome = h2h_market["outcomes"][0]
                            odds = outcome.get("price")
                            if odds:
                                bookmakers.append({
                                    "name": book.get("key"),
                                    "odds": float(odds)
                                })

                if len(bookmakers) > 0:
                    all_matches.append({
                        "match": match_name,
                        "sport": sport,
                        "bookmakers": bookmakers
                    })

        except Exception as e:
            print("❌ ERROR fetching odds:", e)
            print("⏩ Loading from cache instead")
            return _load_cache()

    # Salvează cache la final
    _save_cache(all_matches)
    print(f"\n✅ Total matches collected: {len(all_matches)}")
    return all_matches