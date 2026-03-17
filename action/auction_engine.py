from teams import teams

def update_budget(team, price):

    teams[team]["purse"] -= price


def add_player(team, player):

    teams[team]["players"].append(player)