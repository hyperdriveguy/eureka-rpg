""" File to hold game constants """

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_NAME = "Eureka!"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 2
TILE_SCALING = 2

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 8

PLAYER_START_X = 317
PLAYER_START_Y = 6242

FACE_NONE = 'NONE'
FACE_RIGHT = 'RIGHT'
FACE_LEFT = 'LEFT'
FACE_UP = 'UP'
FACE_DOWN = 'DOWN'

# Map Constants
MAP_PATH = 'project/assets/'
MAPS = {
    'Test Map': 'test_map.json',
    'Test Map 2': 'test_map_2.json'
}

# Enemy Constants
ENEMIES = {
    'cactus': {
        'anim': ['project/assets/angry_cactus.png',
                 'project/assets/angry_cactus_1.png',
                 'project/assets/angry_cactus_2.png'],
        'stats': {
            'HP': 8,
            'Attack': 3,
            'Defense': 0,
            'Skill': 5,
            'Speed': 1
            }
    },
    'pickaxe': {
        'anim': ['project/assets/pickaxe.png',
                 'project/assets/pickaxe_1.png',
                 'project/assets/pickaxe_2.png',
                 'project/assets/pickaxe_3.png',
                 'project/assets/pickaxe_4.png',
                 'project/assets/pickaxe_5.png',
                 'project/assets/pickaxe_6.png',
                 'project/assets/pickaxe_7.png',],
        'stats': {
            'HP': 4,
            'Attack': 4,
            'Defense': 1,
            'Skill': 5,
            'Speed': 8
            }
    }
}
