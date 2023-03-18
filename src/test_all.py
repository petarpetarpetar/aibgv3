import random
from main import *
import heuristics

mapa = object
our_player = object
enemy_player = object


def get_tiles(first, second):
    return mapa.tiles[first], mapa.tiles[second]


def test_directions():
    pairs = [[(1, 1), (3, 0)], [(0, 0), (1, 0)], [(2, 0), (4, 0)]]
    for pair in pairs:
        first, second = pair
        start_tile, end_tile = get_tiles(first, second)
        direction = heuristics.get_direction(start_tile, end_tile)
        direction2 = heuristics.get_direction(end_tile, start_tile)
        num1 = heuristics.count_tiles_between_two_tiles(start_tile, end_tile)
        num2 = heuristics.count_tiles_between_two_tiles(end_tile, start_tile)
        continue
    return


def test_get_dict():
    dic = mapa.get_power_up_positions()
    return


def init():
    global mapa, our_player, enemy_player
    args = parse_arguments()
    game_obj = init_game(args.train, args.bot_vs_bot, args.game_id, args.player_id)
    mapa = get_map(game_obj)
    our_player, enemy_player = get_players(game_obj)


if __name__ == '__main__':
    init()
    test_directions()
    test_get_dict()
