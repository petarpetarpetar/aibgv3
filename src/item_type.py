from enum import Enum


class ItemType(Enum):
    CHERRY_BLOSSOM = 15,
    ROSE = 30
    LILAC = 45
    SUNFLOWER = 60
    ENERGY = 20
    BOOSTER_NECTAR_30_PCT = 30
    BOOSTER_NECTAR_50_PCT = 50
    BOOSTER_NECTAR_100_PCT = 100
    HIVE = 0,
    EMPTY = 0
    POND = 0
    MINUS_FIFTY_PCT_ENERGY = 0
    SUPER_HONEY = 0
    FREEZE = 0
    HOLE = 0

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
