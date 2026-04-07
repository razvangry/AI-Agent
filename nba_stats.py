import requests
import json
from datetime import datetime, timedelta

API_KEY = "abebbd06-efbb-45ea-b791-25fdd0d72e48"
HEADERS = {"Authorization": API_KEY}
BASE_URL = "https://api.balldontlie.io/v1"

# Setează perioada sezonului (poți ajusta)
START_DATE = "2025-10-01"  # început sezon 2025-2026
END_DATE = "2026-04-15"    # sfârșit sezon regular

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def get_games(date_str):
    url = f"{BASE_URL}/games"
    params = {"dates[]": date_str, "per_page": 100}
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10, verify=False)
        response.raise_for_status()
        return response.json()["data"]
    except Exception as e:
        print(f"❌ Error fetching games for {date_str}: {e}")
        return []

def main():
    start_date = datetime.strptime(START_DATE, "%Y-%m-%d")
    end_date = datetime.strptime(END_DATE, "%Y-%m-%d")
    
    all_results = []

    for single_date in daterange(start_date, end_date):
        date_str = single_date.strftime("%Y-%m-%d")
        games = get_games(date_str)
        if not games:
            continue
        
        # sleep 1 secundă între cereri
        time.sleep(1)

        for game in games:
            if game["status"] != "Final":
                continue
            result = {
                "date": date_str,
                "home_team": game["home_team"]["full_name"],
                "visitor_team": game["visitor_team"]["full_name"],
                "home_score": game["home_team_score"],
                "visitor_score": game["visitor_team_score"]
            }
            all_results.append(result)
            print(f"{date_str}: {result['home_team']} {result['home_score']} - {result['visitor_score']} {result['visitor_team']}")

    # Salvează în fișier JSON
    with open("nba_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)
    
    print(f"\n✅ Saved {len(all_results)} results to nba_results.json")

if __name__ == "__main__":
    main()