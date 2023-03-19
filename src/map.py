import item_type as it
import neighbors as nb


class TileContent:
    def __init__(self, item_type):
        self.item_type = it.ItemType[item_type]


class Tile:
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
        self.height, self.width = self.tiles.shape

    def get_neighbor_list(self, current_tile):
        x, y = current_tile.row, current_tile.column
        nb.set_x_y(x, y)
        neighbors_position = [
            nb.neighbor_up_position(),
            nb.neighbor_down_position(),
            nb.neighbor_upper_left_position(),
            nb.neighbor_upper_right_position(),
            nb.neighbor_down_left_position(),
            nb.neighbor_down_right_position(),
        ]
        neighbors = []
        for position in neighbors_position:
            if position is None:
                neighbors.append(None)
            else:
                neighbors.append(self.tiles[x, y])
        return neighbors

    def get_neighbor(self, cursor: Tile, direction: int):
        x, y = cursor.row, cursor.column
        nb.set_x_y(x, y)
        if direction == 0:
            position = nb.neighbor_up_position()
            if position is None:
                return None
            return self.tiles[nb.neighbor_up_position()]

        elif direction == 1:
            position = nb.neighbor_upper_right_position()
            if position is None:
                return None
            return self.tiles[nb.neighbor_upper_right_position()]

        elif direction == 2:
            position = nb.neighbor_down_right_position()

            if position is None:
                return None
            return self.tiles[nb.neighbor_down_right_position()]

        elif direction == 3:
            position = nb.neighbor_down_position()
            if position is None:
                return None
            return self.tiles[nb.neighbor_down_position()]

        elif direction == 4:
            position = nb.neighbor_down_left_position()
            if position is None:
                return None
            return self.tiles[nb.neighbor_down_left_position()]

        elif direction == 5:
            position = nb.neighbor_upper_left_position()
            if position is None:
                return None
            return self.tiles[nb.neighbor_upper_left_position()]

    def get_power_up_positions(self):
        power_dict = {}
        boosters = it.ItemType.get_boosters()
        for item in boosters:
            power_dict[item] = []
        for row in self.tiles:
            for tile in row:
                item_type = tile.tile_content.item_type
                if item_type in boosters:
                    power_dict[item_type].append(tile)
        return power_dict
