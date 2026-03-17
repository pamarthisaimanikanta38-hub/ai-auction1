import random

def evaluate(runs, wickets):

    return runs*0.5 + wickets*20


def alphabeta(depth, alpha, beta, maximizing, value):

    if depth == 0:
        return value

    if maximizing:

        best = -9999

        for _ in range(3):

            score = alphabeta(depth-1, alpha, beta, False, value+random.randint(1,20))

            best = max(best, score)
            alpha = max(alpha, best)

            if beta <= alpha:
                break

        return best

    else:

        best = 9999

        for _ in range(3):

            score = alphabeta(depth-1, alpha, beta, True, value-random.randint(1,20))

            best = min(best, score)
            beta = min(beta, best)

            if beta <= alpha:
                break

        return best


def ai_bid(current_price, purse, runs, wickets):

    value = evaluate(runs, wickets)

    decision = alphabeta(3, -9999, 9999, True, value)

    if decision > current_price and purse > current_price:

        return current_price + random.randint(10,30)

    return None