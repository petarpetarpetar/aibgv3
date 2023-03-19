from map import Map
from player import Player
from item_type import ItemType
from petar import run_BFS
import  heuristics

bee = None
enemy = None
_map = None


def get_data(player_, enemy_, mapa_):
    global bee, enemy, _map
    bee = player_
    enemy = enemy_
    _map = mapa_


def count_tiles_between_two_tiles(tile_list):
    start = tile_list[0]
    count = 0
    for i in range(1, len(tile_list)):
        end = tile_list[i]
        path_len = heuristics.count_tiles_between_two_tiles(start, end)
        count += path_len
        start = end
    return count


def calculate_togo():
    togo = []
    IMPOSSIBLE = 500
    powerups = _map.get_power_up_positions()[ItemType.ENERGY]
    tiles_required = [run_BFS(_map.tiles[bee.x, bee.y], x, _map, (enemy.x, enemy.y), True) for x in powerups]
    moves_required = [tile_required[1] if tile_required is not None else IMPOSSIBLE for tile_required in tiles_required]
    least_required_moves = min(moves_required)

    filtered_tiles = [tile[0] if tile is not None else None for tile in tiles_required if tile[1] == least_required_moves]
    tile_counts = [count_tiles_between_two_tiles(tiles) if tiles is not None else IMPOSSIBLE for tiles in filtered_tiles]
    least_required_tiles = min(tile_counts)
    final_tiles = []
    for i in range(len(filtered_tiles)):
        if tile_counts[i] == least_required_tiles:
            final_tiles.append(filtered_tiles[i])

    return final_tiles
