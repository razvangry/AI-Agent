from data_collector import get_odds
from value_detector import analyze_match
from bankroll import calculate_stake
from tracker import add_bet
from config import BANKROLL


def main():
    print("🚀 Betting Bot Started...\n")

    matches = get_odds()

    analyzed = []

    for match in matches:
        result = analyze_match(match)
        if result:
            analyzed.append(result)

    analyzed.sort(key=lambda x: x["value"], reverse=True)

    top = analyzed[:8]

    for bet in top:
        prob = 1 / bet["sharp_odds"]
        stake = calculate_stake(BANKROLL, bet["best_odds"], prob)

        bet["stake"] = round(stake, 2)

        print("=" * 40)
        print(bet["match"])
        print(f"Odds: {bet['best_odds']} | Sharp: {bet['sharp_odds']}")
        print(f"Edge: {bet['edge']:.3f} | Value: {bet['value']:.3f}")
        print(f"Stake: {bet['stake']}")

        add_bet(bet)


if __name__ == "__main__":
    main()