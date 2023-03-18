import argparse

import numpy as np

from apiCalls import *
from direction import Direction
import map
import time
from petar import run_BFS


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
    print(mapa.get_neighbor(mapa.tiles[0,0], 3))
    run_BFS(mapa.tiles[0,0],mapa.tiles[2, 0], mapa)


if __name__ == "__main__":
    main()
