import arcade
from game import constants

class Contestant(arcade.Sprite):

    def __init__(self):
        self._scale = constants.CHARACTER_SCALING
        self._is_turn = False
        
        # Base Battle Stats
        self._base_heart_points = 10
        self._base_attack = 5
        self._base_defense = 5
        self._base_skill = 5
        self._base_speed = 5
        
        # Current stats/modifiers
        self._cur_heart_points = self._base_heart_points
        self._attack_mod = 0
        self._defense_mod = 0
        self._skill_mod = 0
        self._speed_mod = 0
    
    def update_animation(self, delta_time: float = 1 / 60):
        raise ValueError('"update_animation" was not properly overridden by child.')
    
    @property
    def is_turn(self):
        return self._is_turn

    @is_turn.setter
    def is_turn(self, is_turn: bool):
        self._is_turn = is_turn
    
    @property
    def cur_hp(self):
        return self._cur_heart_points
    
    @cur_hp.setter
    def cur_hp(self, cur_hp: int):
        self._cur_heart_points = cur_hp
    
    @property
    def max_hp(self):
        return self._base_heart_points
