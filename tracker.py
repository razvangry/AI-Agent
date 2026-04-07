import json
import os

FILE = "history.json"


def load_history():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)


def save_history(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_bet(bet):
    history = load_history()

    history.append({
        "match": bet["match"],
        "odds": bet["best_odds"],
        "stake": bet["stake"],
        "closing_odds": None,
        "clv": None
    })

    save_history(history)