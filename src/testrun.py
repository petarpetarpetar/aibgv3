import argparse
import random

import numpy as np

from apiCalls import *
from direction import Direction
import map
import time
from item_type import ItemType
from petar import run_BFS
from player import Player
import heuristics

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

    
    step = run_BFS(mapa.tiles[0, 0], mapa.tiles[1, 7], mapa, (enemy_player.x, enemy_player.y))
    print("PLAYED")
    print(step)
    moves = reversed(step[:-1])
    print("gameId: ", game_obj.get("gameId"))
    
    bee = Player(game_obj.get("player1"))

    #pocetni bee.x, bee.y
    #krajnji m.row, m.column
    while True:
        for m in moves:
            print(m)
            direction = heuristics.get_direction(mapa.tiles[bee.x, bee.y], mapa.tiles[m.row, m.column])
            amount = heuristics.count_tiles_between_two_tiles(mapa.tiles[bee.x, bee.y], mapa.tiles[m.row, m.column])
            print(direction)
            print(amount)
            time.sleep(5)
            game_obj = move(direction, amount)
            bee = Player(game_obj.get("player1"))
            time.sleep(5)


if __name__ == "__main__":
    main()