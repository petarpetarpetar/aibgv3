import math
from direction import Direction
from move import Move


def make_tile_empty(map: dict, row: int, column: int):
    tiles = map.get("tiles")

    for tile_arr in tiles:
        for t in tile_arr:
            if t.get("row") == row and t.get("column") == column:
                t.update({"tileContent": {"itemType": "EMPTY", "numOfItems": 0}})

    map.update({"tiles": tiles})


def update_score_from_nectar(player: dict, prev_score: int, inc: int):
    if player.get("nectar") <= 100:
        player.update({"score": prev_score + inc})


def find_tile(tiles: list, row: int, column: int):
    for tile_arr in tiles:
        for tile in tile_arr:
            if tile.get("row") == row and tile.get("column") == column:
                return tile


def simulate_move(move: Move, tile: dict, game_obj: dict, my_player: str, distance: int):
    player = None
    opp_player = None
    map = game_obj.get("map")

    if my_player == "player1":
        player = game_obj.get("player1")
        opp_player = game_obj.get("player2")

    else:
        opp_player = game_obj.get("player1")
        player = game_obj.get("player2")

    if tile is not None:
        item_type = find_tile(map.get("tiles"), tile.get("row"), tile.get("column")).get("itemType")
    prev_nectar = player.get("nectar")
    prev_energy = player.get("energy")
    prev_honey = player.get("honey")
    prev_score = player.get("score")
    opp_prev_energy = opp_player.get("energy")

    if move == Move.MOVE:
        if item_type == "CHERRY_BLOSSOM":
            player.update({"nectar": prev_nectar + 15})
            update_score_from_nectar(player, prev_score, 15)
        elif item_type == "ROSE":
            player.update({"nectar": prev_nectar + 30})
            update_score_from_nectar(player, prev_score, 30)
        elif item_type == "LILAC":
            player.update({"nectar": prev_nectar + 45})
            update_score_from_nectar(player, prev_score, 45)
        elif item_type == "SUNFLOWER":
            player.update({"nectar": prev_nectar + 60})
            update_score_from_nectar(player, prev_score, 60)
        elif item_type == "ENERGY":
            player.update({"energy": prev_energy + 20})
            player.update({"score": prev_score + 20})
        elif item_type == "BOOSTER_NECTAR_30":
            player.update({"nectar": prev_nectar * 1.3})
            update_score_from_nectar(player, prev_score, prev_nectar - (prev_nectar * 1.3))
        elif item_type == "BOOSTER_NECTAR_50":
            player.update({"nectar": prev_nectar * 1.5})
            update_score_from_nectar(player, prev_score, prev_nectar - (prev_nectar * 1.5))
        elif item_type == "BOOSTER_NECTAR_100":
            player.update({"nectar": prev_nectar * 2})
            update_score_from_nectar(player, prev_score, prev_nectar - (prev_nectar * 2))
        elif item_type == "POND":
            game_obj.update({"winnerTeamName": "other"})
        elif item_type == "MINUS_FIFTY_PCT_ENERGY":
            opp_player.update({"energy": opp_prev_energy * 0.5})
            player.update({"score": prev_score + 50})
        elif item_type == "SUPER_HONEY":
            player.update({"honey": prev_honey + 5})
            player.update({"score": prev_score + 150})
        elif item_type == "FREEZE":
            opp_player.update({"turnsFrozen": 3, "frozen": True})
            player.update({"score": prev_score + 100})

        make_tile_empty(map, tile.get("row"), tile.get("column"))
        player.update({"energy": prev_energy - (distance * 2)})

        if player.get("energy") <= 0:
            game_obj.update({"winnerTeamName": "other"})

        if player.get("nectar") > 100:
            player.update({"nectar": 100})
            player.update({"score": prev_score + (100 - prev_nectar)})

        player.update({"x": tile.get("row"), "y": tile.get("column")})
    elif move == Move.NECTAR_TO_HONEY:
        if player.get("x") != player.get("hiveX") and player.get("y") != player.get("hiveY"):
            return game_obj
        honey_amount = prev_nectar / 20
        player.update({"nectar": prev_nectar % 20, "honey": prev_honey + honey_amount})
        player.update({"score": prev_score + (honey_amount * 30)})
    elif move == Move.NECTAR_TO_ENERGY:
        if player.get("x") != player.get("hiveX") and player.get("y") != player.get("hiveY"):
            return game_obj
        energy_amount = 100 - prev_energy
        player.update({"nectar": prev_nectar - (energy_amount / 2), "energy": prev_energy + energy_amount})
    elif move == Move.SKIP_TURN:
        player.update({"energy": prev_energy + 5})

    if player.get("energy") > 100:
        player.update({"energy": 100})

    if my_player == "player1":
        game_obj.update({"player1": player, "player2": opp_player})
    else:
        game_obj.update({"player1": opp_player, "player2": player})

    return game_obj


def valid_from_tile(tile, direction: Direction):
    valid = []
    current_tile = tile
    distance = 0

    while True:
        if current_tile.get("row") % 2 == 0:
            if direction == direction.down:
                distance += 1
                current_tile.update({"row": current_tile.get("row") + 2, "distance": distance})
            elif direction == direction.up:
                distance += 1
                current_tile.update({"row": current_tile.get("row") - 2, "distance": distance})
            elif direction == direction.up_left:
                distance += 1
                current_tile.update(
                    {"row": current_tile.get("row") - 1, "column": current_tile.get("column") - 1, "distance": distance}
                )
            elif direction == direction.up_right:
                distance += 1
                current_tile.update({"row": current_tile.get("row") - 1, "distance": distance})
            elif direction == direction.down_left:
                distance += 1
                current_tile.update(
                    {"row": current_tile.get("row") + 1, "column": current_tile.get("column") - 1, "distance": distance}
                )
            elif direction == direction.down_right:
                distance += 1
                current_tile.update({"row": current_tile.get("row") + 1, "distance": distance})
        else:
            if direction == direction.down:
                distance += 1
                current_tile.update({"row": current_tile.get("row") + 2, "distance": distance})
            elif direction == direction.up:
                distance += 1
                current_tile.update({"row": current_tile.get("row") - 2, "distance": distance})
            elif direction == direction.up_left:
                distance += 1
                current_tile.update({"row": current_tile.get("row") - 1, "distance": distance})
            elif direction == direction.up_right:
                distance += 1
                current_tile.update(
                    {"row": current_tile.get("row") - 1, "column": current_tile.get("column") + 1, "distance": distance}
                )
            elif direction == direction.down_left:
                distance += 1
                current_tile.update({"row": current_tile.get("row") + 1, "distance": distance})
            elif direction == direction.down_right:
                distance += 1
                current_tile.update(
                    {"row": current_tile.get("row") + 1, "column": current_tile.get("column") + 1, "distance": distance}
                )

        current_tile.update({"direction": direction})

        if current_tile.get("row") < 0 or current_tile.get("row") > 26:
            break
        elif current_tile.get("column") < 0 or current_tile.get("column") > 8:
            break
        elif current_tile.get("column") == 8 and current_tile.get("row") % 2 == 1:
            break

        valid.append(current_tile.copy())

    return valid


def evaluate_state(game_obj: dict, my_player: str):
    score = 0
    opp_player = "player2" if my_player == "player1" else "player1"

    if game_obj.get("winnerTeamName") == "other":
        return -math.inf
    elif game_obj.get("winnerTeamName") == "xepoju":
        return math.inf

    score += game_obj.get(my_player).get("honey") * 30
    score -= game_obj.get(opp_player).get("honey") * 30
    score += game_obj.get(my_player).get("score")
    score -= game_obj.get(opp_player).get("score")
    score += game_obj.get(opp_player).get("frozen") * 100
    score += game_obj.get(my_player).get("nectar")
    score -= game_obj.get(opp_player).get("nectar")
    score += game_obj.get(my_player).get("energy")
    score -= game_obj.get(opp_player).get("energy")

    return score


def get_best_score(game_obj: dict, lookahead_depth: int):
    my_player = "player1"
    player1_obj = game_obj.get("player1")
    player2_obj = game_obj.get("player2")
    my_position = None
    opponent_position = None

    if player1_obj.get("teamName") == "xepoju":
        my_position = {"x": player1_obj.get("x"), "y": player1_obj.get("y")}
        opponent_position = {"x": player2_obj.get("x"), "y": player2_obj.get("y")}
    else:
        opponent_position = {"x": player1_obj.get("x"), "y": player1_obj.get("y")}
        my_position = {"x": player2_obj.get("x"), "y": player2_obj.get("y")}
        my_player = "player2"

    if lookahead_depth == 0:
        return evaluate_state(game_obj.copy(), my_player)

    best_move = None
    best_score = -math.inf
    tiles = game_obj.get("map").get("tiles")
    valid_from_tile_dict = {}
    lookahead_state = None
    move = None

    for m in Move:
        if m == Move.MOVE:
            for d in Direction:
                valid_from_tile_dict[d] = valid_from_tile({"row": my_position.get("x"), "column": my_position.get("y")}, d)

                for tile in valid_from_tile_dict[d]:
                    if (tile.get("row") == my_position.get("x") and tile.get("column") == my_position.get("y")) or (
                        tile.get("row") == opponent_position.get("x") and tile.get("column") == opponent_position.get("y")
                    ):
                        continue

                    lookahead_state = simulate_move(m, tile, game_obj.copy(), my_player, tile.get("distance"))
                    tile.update({"direction": d})
                    move = (m, tile)
                    score = get_best_score(lookahead_state.copy(), lookahead_depth - 1)

                    if score > best_score:
                        best_score = score
                        best_move = move

        else:
            lookahead_state = simulate_move(m, None, game_obj.copy(), my_player, 0)
            move = (m, None)
            score = get_best_score(lookahead_state.copy(), lookahead_depth - 1)

            if score > best_score:
                best_score = score
                best_move = move

    return best_score


def get_best_move(game_obj: dict, lookahead_depth: int):
    """
    game_obj - object representing the state of the game
    lookahead_depth - how many moves in the future you want to look
    """

    my_player = "player1"
    my_position = None
    opponent_position = None
    player1_obj = game_obj.get("player1")
    player2_obj = game_obj.get("player2")

    if player1_obj.get("teamName") == "xepoju":
        my_position = {"x": player1_obj.get("x"), "y": player1_obj.get("y")}
        opponent_position = {"x": player2_obj.get("x"), "y": player2_obj.get("y")}
    else:
        opponent_position = {"x": player1_obj.get("x"), "y": player1_obj.get("y")}
        my_position = {"x": player2_obj.get("x"), "y": player2_obj.get("y")}
        my_player = "player2"

    best_move = None
    best_score = -math.inf
    tiles = game_obj.get("map").get("tiles")
    valid_from_tile_dict = {}
    lookahead_state = None
    move = None

    for m in Move:
        if m == Move.MOVE:
            for d in Direction:
                valid_from_tile_dict[d] = valid_from_tile({"row": my_position.get("x"), "column": my_position.get("y")}, d)

                for tile in valid_from_tile_dict[d]:
                    if tile.get("row") == opponent_position.get("x") and tile.get("column") == opponent_position.get("y"):
                        continue

                    lookahead_state = simulate_move(m, tile, game_obj.copy(), my_player, tile.get("distance"))
                    tile.update({"direction": d})
                    move = (m, tile)
                    score = get_best_score(lookahead_state.copy(), lookahead_depth - 1)

                    if score > best_score:
                        best_score = score
                        best_move = move

        else:
            lookahead_state = simulate_move(m, None, game_obj.copy(), my_player, 0)
            move = (m, None)
            score = get_best_score(lookahead_state.copy(), lookahead_depth - 1)

            if score > best_score:
                best_score = score
                best_move = move

    return (best_move, score)


def evaluate(game_obj: dict, our_player: str):
    opp_player = "player2" if our_player == "player1" else "player1"

    score += game_obj.get(our_player).get("honey") * 30
    score -= game_obj.get(opp_player).get("honey") * 30
    score += game_obj.get(our_player).get("score")
    score -= game_obj.get(opp_player).get("score")
    score += game_obj.get(our_player).get("frozen") * 100
    score += game_obj.get(our_player).get("nectar")
    score -= game_obj.get(opp_player).get("nectar")
    score += game_obj.get(our_player).get("energy")
    score -= game_obj.get(opp_player).get("energy")

    return score


# def valid_moves(game_obj: dict, position: dict, hive: dict):
#     valid_moves_arr = []

#     if position.get("x") == hive.get("x") and position.get("y") == hive.get("y"):
#         valid_moves_arr.append((Move.NECTAR_TO_ENERGY, None))
#         valid_moves_arr.append((Move.NECTAR_TO_HONEY, None))


# def game_over(game_obj: dict):
#     if game_obj.get("winningTeamName") is not None:
#         return True

#     tiles = game_obj.get("map").get("tiles")

#     if game_obj.get("player1").get("energy") <= 0 or game_obj.get("player2").get("energy") <= 0:
#         return True

#     for tile_arr in tiles:
#         for tile in tile_arr:
#             item_type = tile.get("tileContent").get("itemType")
#             if item_type == "CHERRY_BLOSSOM" or item_type == "ROSE" or item_type == "LILAC" or item_type == "SUNFLOWER":
#                 return False

#     return True


# def minimax_alpha_beta_pruning(game_obj, depth, alpha, beta, maximizing_player, our_player):
#     if depth == 0 or game_over(game_obj):
#         return evaluate(game_obj, our_player), None

#     opp_player = 'player2' if our_player == 'player1' else 'player1'

#     if maximizing_player:
#         max_value = -math.inf
#         best_move = None
#         for move in valid_moves(game_obj, {"x": game_obj.get(our_player).get("x"), "y": game_obj.get(our_player).get('y')}, {"x": game_obj.get(our_player).get("hiveX"), "y": game_obj.get(our_player).get('hiveY')}):
#             new_state = make_move(game_obj, move)
#             value, _ = minimax_alpha_beta_pruning(new_state, depth - 1, alpha, beta, False)
#             if value > max_value:
#                 max_value = value
#                 best_move = move
#             alpha = max(alpha, value)
#             if beta <= alpha:
#                 break
#         return max_value, best_move

#     else:  # minimizing player
#         min_value = math.inf
#         best_move = None
#         for move in valid_moves(game_obj, {"x": game_obj.get(opp_player).get("x"), "y": game_obj.get(opp_player).get('y')}, {"x": game_obj.get(opp_player).get("hiveX"), "y": game_obj.get(opp_player).get('hiveY')},):
#             new_state = make_move(game_obj, move)
#             value, _ = minimax_alpha_beta_pruning(new_state, depth - 1, alpha, beta, True)
#             if value < min_value:
#                 min_value = value
#                 best_move = move
#             beta = min(beta, value)
#             if beta <= alpha:
#                 break
#         return min_value, best_move


def populate_item_type(game_obj: dict, valid_tiles_arr: list):
    tiles = game_obj.get("map").get("tiles")

    for tile_arr in tiles:
        for tile in tile_arr:
            for valid_tile in valid_tiles_arr:
                if tile.get("row") == valid_tile.get("row") and tile.get("column") == valid_tile.get("column"):
                    valid_tile.update({"tileContent": tile.get("tileContent")})


def detect_hive(valid_tiles_arr, our_hive):
    for valid_tile in valid_tiles_arr:
        if valid_tile["row"] == our_hive["row"] and valid_tile["column"] == our_hive["column"]:
            return True


def get_move(game_obj: dict, our_player: str, enemy_player: str):
    valid_from_tile_dict = {}

    our_position = {"row": game_obj.get(our_player).get("x"), "column": game_obj.get(our_player).get("y")}
    our_hive = {"row": game_obj.get(our_player).get("hiveX"), "column": game_obj.get(our_player).get("hiveY")}

    enemy_position = {"row": game_obj.get(enemy_player).get("x"), "column": game_obj.get(enemy_player).get("y")}
    flowers = ["CHERRY_BLOSSOM", "ROSE", "LILAC", "SUNFLOWER"]

    for d in Direction:
        valid_from_tile_dict[d] = valid_from_tile(our_position.copy(), d)
        populate_item_type(game_obj, valid_from_tile_dict[d])

    # valid_from_tile_dict ovde sadrzi gde se mozemo kretati, udaljenost i sadrzaj
    max_distance = game_obj.get(our_player).get("energy") / 2
    nectar = game_obj.get(our_player).get("nectar")
    energy = game_obj.get(our_player).get("energy")

    for d in Direction:
        pond_detected = False
        nectar = game_obj.get(our_player).get("nectar")
        for i, tile in enumerate(valid_from_tile_dict[d]):
            if tile["tileContent"]["itemType"] == "POND":
                pond_detected = True
                break

            if (
                game_obj[our_player]["nectar"] > 20
                and our_position["column"] == our_hive["column"]
                and our_position["row"] == our_hive["row"]
            ):
                print("usao", nectar)
                return [(Move.NECTAR_TO_HONEY, 4), (Move.NECTAR_TO_ENERGY, 20)]

            if energy <= 5:
                return [(Move.SKIP_TURN, None)]

            if (
                tile["tileContent"]["itemType"] == "SUPER_HONEY"
                or tile["tileContent"]["itemType"] == "FREEZE"
                or tile["tileContent"]["itemType"] == "MINUS_FIFTY_PCT_ENERGY"
            ):
                return [(Move.MOVE, tile)]

            if nectar == 100:
                # go to hive
                if tile["row"] == our_hive["row"] and tile["column"] == our_hive["column"]:
                    return [(Move.MOVE, tile)]
                if abs(tile["row"] - our_hive["row"]) % 2 == 0:
                    return [(Move.MOVE, tile)]
                if (i + 1) <= valid_from_tile_dict[d] and valid_from_tile_dict[d][i + 1]["tileContent"]["itemType"] == "POND":
                    return [(Move.MOVE, tile)]

            if tile.get("tileContent").get("itemType") in flowers and nectar < 100:
                nectar += tile.get("tileContent").get("numOfItems")

                if nectar >= 100:
                    return [(Move.MOVE, tile)]

        if pond_detected:
            continue
