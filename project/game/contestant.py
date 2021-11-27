import arcade
from game import constants

class Contestant(arcade.Sprite):

    def __init__(self):
        self._scale = constants.CHARACTER_SCALING
        
        # Base Battle Stats
        self._base_heart_points = 10
        self._base_attack = 5
        self._base_defense = 5
        self._base_skill = 5
        self._base_speed = 5
        
        # Current stats/modifiers
        self._cur_heart_points = self._base_heart_points
        self._attack_mod = 1
        self._defense_mod = 1
        self._skill_mod = 1
        self._speed_mod = 1
    
    def update_animation(self, delta_time: float = 1 / 60):
        raise ValueError('"update_animation" was not properly overridden by child.')
