from typing import Iterable
import arcade
from game import constants

class Contestant(arcade.Sprite):

    def __init__(self, idle_pics: Iterable, hp=10, attack=5, defense=5, skill=5, speed=5):
        super().__init__()
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
        
        self._last_text_update = 0
        self._cur_texture = 0
        self._update_direction = 1
        self._idle_textures = []
        for pic in idle_pics:
            self._idle_textures.append(arcade.load_texture(pic))
    
    def update_animation(self, delta_time: float = 1 / 60):
        if self._last_text_update > 1 / 2:
            self._cur_texture += self._update_direction
            if self._cur_texture >= len(self._idle_textures) - 1:
                self._update_direction = -1
            elif self._cur_texture <= 0:
                self._update_direction = 1
            self.texture = self._idle_textures[self._cur_texture] 
        self._last_text_update += delta_time
    
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
