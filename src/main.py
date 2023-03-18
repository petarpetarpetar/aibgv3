import argparse

import numpy as np

from apiCalls import *
from direction import Direction
import src.map as game_map
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
    tiles = np.zeros((27, 9), dtype=game_map.Tile)
    for server_tile_row in server_tile_list:
        for server_tile in server_tile_row:
            tile = game_map.Tile(server_tile)
            tiles[tile.row, tile.column] = tile
    return game_map.Map(tiles)


def get_players(game_obj):
    player1 = Player(game_obj.get("player1"))
    player2 = Player(game_obj.get("player2"))
    our_player = player1
    enemy_player = player2
    if player2.team_name == "xepoju":
        enemy_player = player1
    return our_player, enemy_player


def main():
    args = parse_arguments()
    game_obj = init_game(args.train, args.bot_vs_bot, args.game_id, args.player_id)
    mapa = get_map(game_obj)
    our_player, enemy_player = get_players(game_obj)
    # TODO nas_potez(our_player, enemy_player, mapa)
    print("gameId: ", game_obj.get("gameId"))


if __name__ == "__main__":
    main()
