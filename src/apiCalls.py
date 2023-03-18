import requests as req


def join_game():
    res = req.get(f"http://localhost:8080/joinGame?playerId={player_id}&gameId={game_id}")

    return res.json()


def start_training():
    body = {"playerId": player_id, "playerSpot": 1}
    res = req.post(f"http://localhost:8080/train/makeGame", json=body)

    return res.json()


def bot_vs_bot():
    res = req.get(f"http://localhost:8080/botVSbot?player1Id={player_id}&player2Id={player_id + 1}")

    return res.json()


def init_game(train, bot_vs_bot, _game_id, _player_id):
    global url
    global game_id
    global player_id

    url = "http://localhost:8080/" + "train" if train else ""
    game_id = _game_id
    player_id = _player_id

    if train:
        game_obj = start_training()
        game_id = game_obj.get("gameId")
        return game_obj
    elif bot_vs_bot:
        game_obj = bot_vs_bot()
        game_id = game_obj.get("gameID")
        return game_obj
    elif not train and not bot_vs_bot:
        return join_game()


def move(direction, distance):
    pass
