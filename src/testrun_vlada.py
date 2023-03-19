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
from bestMoves import valid_from_tile, populate_item_type
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
    our_player_str = "player1"
    enemy_player_str = "player2"

    player1 = Player(game_obj.get("player1"))
    player2 = Player(game_obj.get("player2"))
    our_player = player1
    enemy_player = player2
    if player2.team_name == "xepoju":
        enemy_player = player1
        our_player = player2
        enemy_player_str = "player1"
        our_player_str = "player2"

    print("gameId: ", game_obj.get("gameId"))
    time.sleep(5)
    bee = Player(game_obj.get(our_player_str))
    flowers = ["CHERRY_BLOSSOM", "ROSE", "LILAC", "SUNFLOWER"]

    while True:
        togo = [mapa.tiles[26, 0], mapa.tiles[22, 1], mapa.tiles[0, 8], mapa.tiles[4, 7]]
        # togo_honey = mapa.get_power_up_positions()[ItemType.SUPER_HONEY]
        # togo_freeze = mapa.get_power_up_positions()[ItemType.FREEZE]
        # togo_energy = mapa.get_power_up_positions()[ItemType.ENERGY]
        # togo = togo_honey + togo_freeze + togo_energy
        # for go in togo:
        #     while True:
        #         if bee.x == go.row and bee.y == go.column:
        #             break
        #         print("bee", bee.x, bee.y)
        #         print("go", go)
        #         steps = run_BFS(mapa.tiles[bee.x, bee.y], go, mapa, (enemy_player.x, enemy_player.y))

        #         if mapa.tiles[bee.x, bee.y] in steps:
        #             steps.remove(mapa.tiles[bee.x, bee.y])

        #         moves = steps[::-1]
        #         # moves = moves[1:]

        #         bee = Player(game_obj.get("player1"))

        #         for s in moves:
        #             print(s, end=" |")
        #         time.sleep(1)
        #         m = moves[0]
        #         print(m)
        #         direction = heuristics.get_direction(mapa.tiles[bee.x, bee.y], mapa.tiles[m.row, m.column])
        #         amount = heuristics.count_tiles_between_two_tiles(mapa.tiles[bee.x, bee.y], mapa.tiles[m.row, m.column])
        #         print("direction", direction)
        #         print("amount", amount)

        #         game_obj = move(direction, amount)
        #         mapa = get_map(game_obj)
        #         time.sleep(3)
        #         bee = Player(game_obj.get("player1"))

        while True:
            # ide se u kosnicu ako ima dovoljno nektara
            if bee.energy < 5:
                game_obj = skip_a_turn()
                mapa = get_map(game_obj)
                bee = Player(game_obj.get(our_player_str))
                enemy_player = Player(game_obj.get(enemy_player_str))

            if bee.nectar >= 90:
                go = mapa.tiles[bee.hive_x, bee.hive_y]

                while True:
                    if bee.x == go.row and bee.y == go.column:
                        break
                    print("bee", bee.x, bee.y)
                    print("go", go)
                    steps = run_BFS(mapa.tiles[bee.x, bee.y], go, mapa, (enemy_player.x, enemy_player.y))

                    if mapa.tiles[bee.x, bee.y] in steps:
                        steps.remove(mapa.tiles[bee.x, bee.y])

                    moves = steps[::-1]
                    # moves = moves[1:]

                    bee = Player(game_obj.get(our_player_str))
                    enemy_player = Player(game_obj.get(enemy_player_str))

                    for s in moves:
                        print(s, end=" |")
                    time.sleep(1)
                    m = moves[0]
                    print(m)
                    direction = heuristics.get_direction(mapa.tiles[bee.x, bee.y], mapa.tiles[m.row, m.column])
                    amount = heuristics.count_tiles_between_two_tiles(mapa.tiles[bee.x, bee.y], mapa.tiles[m.row, m.column])
                    print("direction", direction)
                    print("amount", amount)

                    if amount * 2 >= bee.energy:
                        game_obj = skip_a_turn()
                    else:
                        game_obj = move(direction, amount)
                    mapa = get_map(game_obj)
                    time.sleep(0.1)
                    bee = Player(game_obj.get(our_player_str))
                    enemy_player = Player(game_obj.get(enemy_player_str))

                game_obj = feed_bee_with_nectar((100 - bee.energy) / 2)
                game_obj = convert_nectar_to_honey(5)
                mapa = get_map(game_obj)
                bee = Player(game_obj.get(our_player_str))
                enemy_player = Player(game_obj.get(enemy_player_str))

            # inace ide se na random polje koje nije pond
            else:
                while True:
                    go: map.Tile = mapa.tiles[random.randint(0, mapa.height - 1), random.randint(0, mapa.width - 1)]

                    if go.column == 8 and go.row % 2 != 0:
                        continue

                    if (
                        go is not None
                        and go.tile_content.item_type != ItemType.POND
                        and go.tile_content.item_type != ItemType.HIVE
                        and go.tile_content.item_type != ItemType.EMPTY
                    ):
                        break

                while True:
                    if bee.nectar == 100:
                        break
                    if bee.x == go.row and bee.y == go.column:
                        break
                    print("bee", bee.x, bee.y)
                    print("go", go)
                    steps = run_BFS(mapa.tiles[bee.x, bee.y], go, mapa, (enemy_player.x, enemy_player.y))

                    if mapa.tiles[bee.x, bee.y] in steps:
                        steps.remove(mapa.tiles[bee.x, bee.y])

                    [print(x) for x in steps]
                    moves = steps[::-1]
                    # moves = moves[1:]

                    bee = Player(game_obj.get(our_player_str))
                    enemy_player = Player(game_obj.get(enemy_player_str))

                    for s in moves:
                        print(s, end=" |")
                    time.sleep(1)
                    m = moves[0]
                    print(m)
                    direction = heuristics.get_direction(mapa.tiles[bee.x, bee.y], mapa.tiles[m.row, m.column])
                    amount = heuristics.count_tiles_between_two_tiles(mapa.tiles[bee.x, bee.y], mapa.tiles[m.row, m.column])
                    print("direction", direction)
                    print("amount", amount)

                    if amount * 2 >= bee.energy:
                        game_obj = skip_a_turn()
                    else:
                        valid_from_tile_arr = valid_from_tile({"row": our_player.x, "column": our_player.y}, direction)
                        populate_item_type(game_obj, valid_from_tile_arr)
                        current_nectar = bee.nectar
                        new_amount = 0

                        for valid_tile in valid_from_tile_arr:
                            if valid_tile.get("tileContent").get("itemType") in flowers:
                                current_nectar += valid_tile.get("tileContent").get("numOfItems")

                            new_amount += 1
                            if current_nectar >= 100 or new_amount >= amount:
                                break

                        if new_amount == 0:
                            new_amount = amount

                        if new_amount * 2 >= bee.energy:
                            game_obj = skip_a_turn()

                        print(f"new_amount {new_amount}, amount {amount}")
                        game_obj = move(direction, new_amount)
                    mapa = get_map(game_obj)
                    time.sleep(0.1)
                    bee = Player(game_obj.get(our_player_str))
                    enemy_player = Player(game_obj.get(enemy_player_str))


if __name__ == "__main__":
    main()
