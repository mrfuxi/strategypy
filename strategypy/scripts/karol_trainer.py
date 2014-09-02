import sys
import os
import json
import itertools
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from game import Game


def log_action(action, ctx):
    radius = 10

    position = ctx["position"]
    player_pk = ctx["player_pk"]
    me = set(ctx["current_data"][player_pk].values())
    enemy_pk = [pk for pk in ctx["current_data"] if pk != player_pk]
    enemies = set(
        itertools.chain(
            *[ctx["current_data"][pk].values() for pk in enemy_pk]
        )
    )

    cells = itertools.product(
        xrange(-radius+position[0], radius+position[0]+1),
        xrange(-radius+position[1], radius+position[1]+1),
    )
    cells = [c for c in cells]

    vector = [action]
    for cell in cells:
        if cell in me:
            val = -1
        elif cell in enemies:
            val = 1
        else:
            val = 0

        vector.append(val)

    return vector


def play_game(p1, p2):
    game = Game(p1, p2)
    game.main_loop()

    if not os.path.exists("data"):
        os.makedirs("data")

    file_name = "{}-{}-{}.json".format(p1, p2, time.time())

    with open("data/{}".format(file_name), "w") as f:
        json.dump(game.get_winner().actions, f)

if __name__ == '__main__':
    for x in xrange(100):
        play_game('davide', 'happiness')
