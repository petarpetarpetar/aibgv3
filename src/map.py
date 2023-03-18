import item_type as it
import numpy as np
import neighbours as nb


class TileContent:
    def __init__(self, item_type):
        self.item_type = it.ItemType[item_type]


class Tile:
    def __init__(self, row, column, tile_content):
        self.row = row
        self.column = column
        self.tile_content = tile_content

    def __init__(self, tile_dict):
        self.row = tile_dict.get("row")
        self.column = tile_dict.get("column")
        tile_content = TileContent(tile_dict.get("tileContent").get("itemType").upper())
        self.tile_content = tile_content

    def __eq__(self, other):
        if self.row == other.row and self.column == other.column and self.tile_content == other.tile_content:
            return True
        else:
            return False
    
    def __str__(self) -> str:
        return f"{self.row} {self.column}"


class Map:
    def __init__(self, tiles):
        self.tiles = tiles
        self.width, self.height = self.tiles.shape

    def get_neigbor_list(self, current_tile):
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

    def get_neighbor(self, cursor: Tile, direction: int) -> Tile:
        x, y = cursor.row, cursor.column
        nb.set_x_y(x, y)
        if direction == 0:
            coords = nb.neighbour_up_position()
            if coords is None:
                return None
            return self.tiles[nb.neighbour_up_position()]
        
        elif direction == 1:
            coords = nb.neighbour_upper_right_position()
            if coords is None:
                return None
            return self.tiles[nb.neighbour_upper_right_position()]
        
        elif direction == 2:
            coords = nb.neighbour_down_right_position()
            
            if coords is None:
                return None
            return self.tiles[nb.neighbour_down_right_position()]
        
        elif direction == 3:
            coords = nb.neighbour_down_position()
            if coords is None:
                return None
            return self.tiles[nb.neighbour_down_position()]
        
        elif direction == 4:
            coords = nb.neighbour_down_left_position()
            if coords is None:
                return None
            return self.tiles[nb.neighbour_down_left_position()]
        
        elif direction == 5:
            coords = nb.neighbour_upper_left_position()
            if coords is None:
                return None
            return self.tiles[nb.neighbour_upper_left_position()]
