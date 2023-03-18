import argparse

import numpy as np

from apiCalls import *
from direction import Direction
import map as game_map
from player import Player
from bestMoves import get_best_move
from move import Move


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


def main():
    args = parse_arguments()
    game_obj = init_game(args.train, args.bot_vs_bot, args.game_id, args.player_id)
    mapa = get_map(game_obj)
    player1 = Player(game_obj.get("player1"))
    player2 = Player(game_obj.get("player2"))
    our_player_str = "player1"
    our_player = player1
    enemy_player = player2
    if player2.team_name == "xepoju":
        enemy_player = player1
        our_player = player2
        our_player_str = "player2"
    # TODO nas_potez(our_player, enemy_player, mapa)
    print("gameId: ", game_obj.get("gameId"))

    while True:
        best_move = get_best_move(game_obj.copy(), 3)
        print(best_move)
        action, tile = best_move

        if action == Move.MOVE:
            game_obj = move(tile.get("direction"), tile.get("distance"))
        elif action == Move.NECTAR_TO_ENERGY:
            amount = (100 - game_obj.get(our_player_str).get("energy")) / 2
            game_obj = feed_bee_with_nectar(amount)
        elif action == Move.NECTAR_TO_HONEY:
            amount = game_obj.get(our_player_str).get("nectar") / 20
            game_obj = convert_nectar_to_honey(amount)
        elif action == Move.SKIP_TURN:
            game_obj = skip_a_turn()


if __name__ == "__main__":
    main()
