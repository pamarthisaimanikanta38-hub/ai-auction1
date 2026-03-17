import random

def evaluate_player(runs,wickets):

    score = runs*0.02 + wickets*2
    return score


def alpha_beta_bid(base_price,runs,wickets,purse):

    value = evaluate_player(runs,wickets)

    bid = base_price + int(value*10)

    if bid > purse:
        return None

    return bid