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
MAP_PATH = 'project/assets/maps/'
MAPS = {
    'Test Map': 'test_map.json',
    'Test Map 2': 'test_map_2.json'
}

# Overworld Constants
OVERWORLD_SPRITE_PATH = 'project/assets/overworld_sprites/'
PLAYER_TEXTURES = {
    'front': {
        'still': f'{OVERWORLD_SPRITE_PATH}overworld_player_still.png',
        'step': f'{OVERWORLD_SPRITE_PATH}overworld_player_step.png'
    },
    'back': {
        'still': f'{OVERWORLD_SPRITE_PATH}overworld_player_back_still.png',
        'step': f'{OVERWORLD_SPRITE_PATH}overworld_player_back_step.png'
    },
    'side': {
        'still': f'{OVERWORLD_SPRITE_PATH}overworld_player_side_still.png',
        'step': f'{OVERWORLD_SPRITE_PATH}overworld_player_side_step.png',
        'alt': f'{OVERWORLD_SPRITE_PATH}overworld_player_side_step_alt.png'
    }

}

# Enemy Constants
ENEMY_SPRITE_PATH = 'project/assets/battle_sprites/'
CONTESTANTS = {
    'player': {
        'anim': [f'{ENEMY_SPRITE_PATH}player/battle_player.png',
                 f'{ENEMY_SPRITE_PATH}player/battle_player_1.png',
                 f'{ENEMY_SPRITE_PATH}player/battle_player_2.png'],
        'stats': {
            'HP': 10,
            'Attack': 5,
            'Defense': 2,
            'Skill': 5,
            'Speed': 5
            }
    },
    'cactus': {
        'anim': [f'{ENEMY_SPRITE_PATH}cactus/angry_cactus.png',
                 f'{ENEMY_SPRITE_PATH}cactus/angry_cactus_1.png',
                 f'{ENEMY_SPRITE_PATH}cactus/angry_cactus_2.png'],
        'stats': {
            'HP': 8,
            'Attack': 3,
            'Defense': 0,
            'Skill': 5,
            'Speed': 1
            }
    },
    'pickaxe': {
        'anim': [f'{ENEMY_SPRITE_PATH}pickaxe/pickaxe.png',
                 f'{ENEMY_SPRITE_PATH}pickaxe/pickaxe_1.png',
                 f'{ENEMY_SPRITE_PATH}pickaxe/pickaxe_2.png',
                 f'{ENEMY_SPRITE_PATH}pickaxe/pickaxe_3.png',
                 f'{ENEMY_SPRITE_PATH}pickaxe/pickaxe_4.png',
                 f'{ENEMY_SPRITE_PATH}pickaxe/pickaxe_5.png',
                 f'{ENEMY_SPRITE_PATH}pickaxe/pickaxe_6.png',
                 f'{ENEMY_SPRITE_PATH}pickaxe/pickaxe_7.png'],
        'stats': {
            'HP': 4,
            'Attack': 40,
            'Defense': 1,
            'Skill': 5,
            'Speed': 8
            }
    }
}
