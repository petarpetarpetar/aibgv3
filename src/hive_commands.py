from map import Map
from player import Player
from item_type import ItemType
from petar import run_BFS

bee = None
enemy = None
_map = None


def get_data(player_, enemy_, mapa_):
    global bee, enemy, _map
    bee = player_
    enemy = enemy_
    _map = mapa_


def count_tiles_between_two_tiles(tile_list):
    pass

def calculate_togo():
    togo = []

    powerups = _map.get_power_up_positions()[ItemType.ENERGY]
    tiles_required = [run_BFS(_map.tiles[bee.x, bee.y], x, _map, (enemy.x, enemy.y), True) for x in powerups]
    moves_required = [tile_required[1] if tile_required is not None else 100 for tile_required in tiles_required]
    least_required_moves = min(moves_required)

    filtered_tiles = [tile[0] if tile is not None else None for tile in tiles_required if tile[1] == least_required_moves]
    return filtered_tiles[0]
