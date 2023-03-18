import numpy as np
import neighbours as nb


class TileContent:
    def __init__(self, item_type):
        self.item_type = item_type


class Tile:
    def __init__(self, row, column, tile_content):
        self.row = row
        self.column = column
        self.tile_content = tile_content

    def __eq__(self, other):
        if self.row == other.row and self.column == other.column and self.tile_content == other.tile_content:
            return True
        else:
            return False


class Map:
    def __init__(self, tiles):
        self.tiles = tiles
        self.width, self.height = self.tiles.shape

    def getNeighborsList(self, current_tile):
        x, y = current_tile.x, current_tile.y
        nb.set_x_y(x, y)
        neighbours_position = [nb.neighbour_up_position(), nb.neighbour_down_position(),
                               nb.neighbour_upper_left_position(), nb.neighbour_upper_right_position(),
                               nb.neighbour_down_left_position(), nb.neighbour_down_right_position()]
        neighbours = []
        for position in neighbours_position:
            if position is None:
                neighbours.append(None)
            else:
                neighbours.append(self.tiles[x, y])
        return neighbours

    def getNeighbor(cursor: Tile, direction: int, _map: None) -> Tile:
        if direction == 0:
            pass
        elif direction == 1:
            pass
        elif direction == 2:
            pass
        elif direction == 3:
            pass
        elif direction == 4:
            pass
        elif direction == 5:
            pass
            