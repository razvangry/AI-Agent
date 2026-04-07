def calculate_stake(bankroll, odds, prob):
    if odds <= 1:
        return 0

    kelly = (prob * odds - 1) / (odds - 1)

    if kelly <= 0:
        return 0

    stake = bankroll * kelly * 0.5

    max_stake = bankroll * 0.02

    return min(stake, max_stake)