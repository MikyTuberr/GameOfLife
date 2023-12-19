from enum import Enum


# POSSIBLE DIRECTIONS TO MOVE
class KeyAction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4
    UP_LEFT = 5
    UP_RIGHT = 6
    DOWN_LEFT = 7
    DOWN_RIGHT = 8
    SPECIAL_ABILITY = 9
    NONE = 10
