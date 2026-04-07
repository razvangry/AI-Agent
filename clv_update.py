from tracker import load_history, save_history
from data_collector import get_odds
from sharp_detector import get_sharp_odds


def update_clv():
    history = load_history()
    matches = get_odds()

    match_map = {m["match"]: m for m in matches}

    for bet in history:
        match_name = bet.get("match")

        if match_name not in match_map:
            continue

        match = match_map[match_name]
        sharp = get_sharp_odds(match["bookmakers"])

        if not sharp:
            continue

        bet["closing_odds"] = sharp
        bet["clv"] = sharp / bet["odds"]

    save_history(history)

    for bet in history:
        if bet["clv"] is None:
            continue

        result = "✔ WIN" if bet["clv"] > 1 else "❌ LOSE"

        print(f"{bet['match']} | CLV: {bet['clv']:.3f} | {result}")