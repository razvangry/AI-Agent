from sharp_detector import get_sharp_odds


def analyze_match(match):
    if not match or "bookmakers" not in match:
        return None

    bookmakers = match["bookmakers"]

    if len(bookmakers) < 3:
        return None

    sharp_odds = get_sharp_odds(bookmakers)

    if not sharp_odds:
        return None

    market_odds_list = [
        bm["odds"] for bm in bookmakers
        if bm.get("name") not in ["pinnacle", "betfair", "matchbook"]
    ]

    if len(market_odds_list) < 2:
        return None

    market_odds = sum(market_odds_list) / len(market_odds_list)

    prob = 1 / sharp_odds
    edge = market_odds / sharp_odds
    value = (prob * market_odds) - 1

    if edge < 1.07 or value < 0.05 or market_odds > 3.0:
        return None

    best = max(bookmakers, key=lambda x: x["odds"])

    return {
        "match": match["match"],
        "sport": match["sport"],
        "best_odds": best["odds"],
        "bookmaker": best["name"],
        "sharp_odds": sharp_odds,
        "market_odds": market_odds,
        "edge": edge,
        "value": value
    }