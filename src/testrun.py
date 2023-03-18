import argparse
import random

import numpy as np

from apiCalls import *
from direction import Direction
import map
import time
from petar import run_BFS
from player import Player


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("train", type=bool)
    parser.add_argument("bot_vs_bot", type=bool)
    parser.add_argument("game_id", type=int)
    parser.add_argument("player_id", type=int)
    args = parser.parse_args()

    return args


def get_map(game_obj):
    map_from_server = game_obj.get("map")
    server_tile_list = map_from_server.get("tiles")
    tiles = np.zeros((27, 9), dtype=map.Tile)
    for server_tile_row in server_tile_list:
        for server_tile in server_tile_row:
            tile = map.Tile(server_tile)
            tiles[tile.row, tile.column] = tile
    return map.Map(tiles)


def main():
    args = parse_arguments()
    game_obj = init_game(args.train, args.bot_vs_bot, args.game_id, args.player_id)
    mapa = get_map(game_obj)
    print("gameId: ", game_obj.get("gameId"))

    player1 = Player(game_obj.get("player1"))
    player2 = Player(game_obj.get("player2"))
    our_player = player1
    enemy_player = player2
    if player2.team_name == "xepoju":
        enemy_player = player1

    cilj_x = random.randint(0,26)
    cilj_y = random.randint(0,9)
    iter = 0
    step = run_BFS(mapa.tiles[0, 0], mapa.tiles[cilj_x, cilj_y], mapa, (enemy_player.x, enemy_player.y))
    while True:
        print("move")
        print(f"{step}")
        step = run_BFS(mapa.tiles[step.row, step.column], mapa.tiles[cilj_x, cilj_y], mapa,
                       (enemy_player.x, enemy_player.y))
        if step is None:
            break


if __name__ == "__main__":
    main()