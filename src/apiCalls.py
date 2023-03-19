import requests as req
from direction import Direction


def join_game():
    res = req.get(f"http://localhost:8082/joinGame?playerId={player_id}&gameId={game_id}")

    return res.json()


def start_training():
    body = {"playerId": player_id, "playerSpot": 1}
    res = req.post(f"http://localhost:8082/train/makeGame", json=body)

    return res.json()


def bot_vs_bot():
    res = req.get(f"http://localhost:8082/botVSbot?player1Id={player_id}&player2Id={player_id + 1}")

    return res.json()


def init_game(train: bool, _bot_vs_bot: bool, _game_id: int, _player_id: int):
    global url
    global game_id
    global player_id

    url = "http://localhost:8082/" + "train/" if train else ""
    game_id = _game_id
    player_id = _player_id

    if train:
        game_obj = start_training()
        game_id = game_obj.get("gameId")
        return game_obj
    elif _bot_vs_bot:
        game_obj = bot_vs_bot()
        game_id = game_obj.get("gameID")
        return game_obj
    elif not train and not _bot_vs_bot:
        return join_game()


def move(direction: Direction, distance: int):
    """
    direction - Enum Direction
    distance - How far you want to go in the desired direction
    """
    body = {"playerId": player_id, "gameId": game_id, "direction": direction.value, "distance": distance}
    res = req.post(url + "move", json=body)
    # print(res.json())
    return res.json()


def convert_nectar_to_honey(amount: int):
    """
    amount - Amount of honey to make (20 nectar for 1 honey)
    """
    body = {"playerId": player_id, "gameId": game_id, "amountOfHoneyToMake": amount}
    res = req.post(url + "convertNectarToHoney", json=body)

    return res.json()


def feed_bee_with_nectar(amount: int):
    """
    amount - Amount of nectar to feed to the bee (1 nectar for 2 energy)
    """
    body = {"playerId": player_id, "gameId": game_id, "amountOfNectarToFeedWith": amount}
    res = req.post(url + "feedBeeWithNectar", json=body)

    return res.json()


def skip_a_turn():
    body = {"playerId": player_id, "gameId": game_id}
    res = req.post(url + "skipATurn", json=body)

    return res.json()
