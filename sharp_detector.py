def get_sharp_odds(bookmakers):
    if not bookmakers:
        return None

    priority = ["pinnacle", "betfair", "matchbook"]

    for sharp in priority:
        for bm in bookmakers:
            if bm.get("name") == sharp:
                return bm.get("odds")

    return None