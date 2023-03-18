import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("train", type=bool)
    parser.add_argument("game_id", type=str)
    parser.add_argument("player_id", type=str)
    args = parser.parse_args()

    return args


def main():
    args = parse_arguments()
    print(args)


if __name__ == "__main__":
    main()
