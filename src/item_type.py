from enum import Enum


class ItemType(Enum):
    CHERRY_BLOSSOM = 15,
    ROSE = 31
    LILAC = 45
    SUNFLOWER = 60
    ENERGY = 20
    BOOSTER_NECTAR_30_PCT = 30
    BOOSTER_NECTAR_50_PCT = 50
    BOOSTER_NECTAR_100_PCT = 100
    HIVE = 0,
    EMPTY = 1
    POND = 2
    MINUS_FIFTY_PCT_ENERGY = 3
    SUPER_HONEY = 4
    FREEZE = 5
    HOLE = 6

    @staticmethod
    def get_boosters():
        boosters = [ItemType.BOOSTER_NECTAR_50_PCT, ItemType.BOOSTER_NECTAR_30_PCT,
                    ItemType.BOOSTER_NECTAR_100_PCT, ItemType.ENERGY, ItemType.MINUS_FIFTY_PCT_ENERGY,
                    ItemType.FREEZE, ItemType.SUPER_HONEY]
        return boosters

    @staticmethod
    def get_flowers():
        flowers = [ItemType.CHERRY_BLOSSOM, ItemType.LILAC, ItemType.ROSE, ItemType.SUNFLOWER]
        return flowers

    @staticmethod
    def get_traps():
        return [ItemType.POND, ItemType.HOLE]

    @staticmethod
    def get_value(item):
        return (int(item) % 10) * 10
