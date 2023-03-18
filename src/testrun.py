import argparse
from apiCalls import *
from direction import Direction
import time

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("train", type=bool)
    parser.add_argument("bot_vs_bot", type=bool)
    parser.add_argument("game_id", type=int)
    parser.add_argument("player_id", type=int)
    args = parser.parse_args()

    return args


def main():
    args = parse_arguments()
    game_obj = init_game(args.train, args.bot_vs_bot, args.game_id, args.player_id)
    print("gameId: ", game_obj.get("gameId"))

    while True:
        # Controll game loop
        time.sleep(1)
        
        game_obj = move(Direction.down, 1)
        

if __name__ == "__main__":
    main()
