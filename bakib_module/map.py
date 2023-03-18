class TileContent:
    def __init__(self, item_type):
        self._item_type = item_type


class Tile:
    def __init__(self, row, column, tile_content):
        self._row = row
        self._column = column
        self._tile_content = tile_content


class Map:
    def __init__(self, tiles):
        self._width = 9
        self._height = 9
        self._tiles = tiles

    def get_element_neighbors(self):
        # TODO
        return

