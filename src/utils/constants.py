# src/utils/constants.py
from enum import Enum, auto


class Direction(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()

    @classmethod
    def opposite(cls, direction):
        return {
            cls.UP: cls.DOWN,
            cls.DOWN: cls.UP,
            cls.LEFT: cls.RIGHT,
            cls.RIGHT: cls.LEFT,
        }[direction]


class RayOutcome(Enum):
    HIT = auto()
    REFLECTION = auto()
    MISS = auto()


# Game settings
DEFAULT_GRID_SIZE = 8
DEFAULT_ATOM_COUNT = 4
INITIAL_POINTS = 25
POINTS_PER_RAY = -1
POINTS_PER_INCORRECT_GUESS = -5
POINTS_PER_CORRECT_GUESS = 10
DEFAULT_DIFFICULTY = "medium"

# Colors (RGB)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255,255,0)

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
