from map import Tile
from direction import Direction


def compare_ints(a, b):
    if a < b:
        return -1
    elif a > b:
        return 1
    else:
        return 0


def get_direction(start: Tile, end: Tile):
    comparison = compare_ints(start.column, end.column)
    if comparison == 0:
        if (start.row - end.row) % 2 == 0:
            direction = Direction.down
            if start.row > end.row:
                direction = Direction.up
            return direction
        if start.row % 2 == 0:
            if start.row > end.row:
                return Direction.up_right
            else:
                return Direction.down_right
        else:
            if start.row > end.row:
                return Direction.up_left
            else:
                return Direction.down_left
    elif comparison == -1:
        if start.row > end.row:
            return Direction.up_right
        else:
            return Direction.down_right
    else:
        if start.row > end.row:
            return Direction.up_left
        else:
            return Direction.down_left


def count_tiles_between_two_tiles(start: Tile, end: Tile):
    # moraju biti direktno povezane
    directions = get_direction(start, end)
    if directions in [Direction.up, Direction.down]:
        return abs(start.row - start.column) % 2
    else:
        return abs(start.row - end.row)
