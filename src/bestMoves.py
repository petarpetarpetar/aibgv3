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
        item_type = tile.get("tileContent").get("itemType")
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


def check_in_arr(tile, arr):
    for elem in arr:
        if tile.get("row") == elem.get("row") and tile.get("column") == elem.get("column"):
            return (True, elem.get("distance"))

    return (False, 0)


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
        return evaluate_state(game_obj, my_player)

    best_move = None
    best_score = -math.inf
    tiles = game_obj.get("map").get("tiles")
    valid_from_tile_dict = {}
    lookahead_state = None
    move = None
    distance = 0
    # treba dodati da li moze u jednom pravcu tu da ode
    for m in Move:
        if m == Move.MOVE:
            for tile_arr in tiles:
                for tile in tile_arr:
                    last_direction = None
                    for d in Direction:
                        valid_from_tile_dict[d.value] = valid_from_tile(
                            {"row": my_position.get("x"), "column": my_position.get("y")}, d
                        )
                        check, distance = check_in_arr(tile, valid_from_tile_dict[d.value])
                        last_direction = d
                        if check:
                            break
                    else:
                        continue

                    if (tile.get("row") == my_position.get("x") and tile.get("column") == my_position.get("y")) or (
                        tile.get("row") == opponent_position.get("x") and tile.get("column") == opponent_position.get("y")
                    ):
                        continue

                    lookahead_state = simulate_move(m, tile, game_obj.copy(), my_player, distance)
                    tile.update({"distance": distance, "direction": last_direction})
                    move = (m, tile)
                    score = get_best_score(lookahead_state, lookahead_depth - 1)

                    if score > best_score:
                        best_score = score
                        best_move = move

        else:
            lookahead_state = simulate_move(m, None, game_obj.copy(), my_player, 0)
            move = (m, None)
            score = get_best_score(lookahead_state, lookahead_depth - 1)

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
    distance = 0
    # treba dodati da li moze u jednom pravcu tu da ode
    for m in Move:
        if m == Move.MOVE:
            for tile_arr in tiles:
                for tile in tile_arr:
                    last_direction = None
                    for d in Direction:
                        valid_from_tile_dict[d.value] = valid_from_tile(
                            {"row": my_position.get("x"), "column": my_position.get("y")}, d
                        )
                        check, distance = check_in_arr(tile, valid_from_tile_dict[d.value])
                        last_direction = d
                        if check:
                            break
                    else:
                        continue

                    if (tile.get("row") == my_position.get("x") and tile.get("column") == my_position.get("y")) or (
                        tile.get("row") == opponent_position.get("x") and tile.get("column") == opponent_position.get("y")
                    ):
                        continue

                    lookahead_state = simulate_move(m, tile, game_obj.copy(), my_player, distance)
                    tile.update({"distance": distance, "direction": last_direction})
                    move = (m, tile)
                    score = get_best_score(lookahead_state, lookahead_depth - 1)

                    if score > best_score:
                        best_score = score
                        best_move = move

        else:
            lookahead_state = simulate_move(m, None, game_obj.copy(), my_player, 0)
            move = (m, None)
            score = get_best_score(lookahead_state, lookahead_depth - 1)

            if score > best_score:
                best_score = score
                best_move = move

    return best_move
