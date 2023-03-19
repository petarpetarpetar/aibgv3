from map import Map
from player import Player
from item_type import ItemType
from petar import run_BFS

bee = Player(None)
enemy = Player(None)
_map = Map(None)


def get_data(player_, enemy_, mapa_):
    global bee, enemy, _map
    bee = player_
    enemy = enemy_
    _map = mapa_


def calculate_togo():
    togo = []

    powerups = _map.get_power_up_positions()[ItemType.ENERGY]

    moves_required = [run_BFS(_map.tiles[bee.x, bee.y], x, _map, (enemy.x, enemy.y), True)[1] for x in powerups]
    print()
    print(moves_required)
    least_required_moves = min(moves_requireds)
    pass