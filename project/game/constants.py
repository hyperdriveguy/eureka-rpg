from enum import Enum, auto


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_NAME = "Eureka!"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 2
TILE_SCALING = 2
COIN_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 8

PLAYER_START_X = 317
PLAYER_START_Y = 6242

class Direction(Enum):
    FACE_NONE = 0
    FACE_RIGHT = 1
    FACE_LEFT = 2
    FACE_UP = 3
    FACE_DOWN = 4
