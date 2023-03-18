from enum import Enum


class Direction(str, Enum):
    up_left = "q"
    up = ("w",)
    up_right = ("e",)
    down_right = ("d",)
    down = ("s",)
    down_left = "a"
