from typing import Iterable
import arcade
from game import constants
from random import randint

class Contestant(arcade.Sprite):

    def __init__(self, idle_pics: Iterable, hp=10, attack=5, defense=5, skill=5, speed=5):
        super().__init__()
        self._scale = constants.CHARACTER_SCALING
        self._is_turn = False
        
        # Base Battle Stats
        self._base_heart_points = 10
        self._base_attack = 10
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
        self._anim_speed = 1
        self._anim_timer = 0
        self._idle_textures = []
        for pic in idle_pics:
            self._idle_textures.append(arcade.load_texture(pic))
    
    def update_animation(self, delta_time: float = 1 / 60):
        if self._last_text_update > 1 / (4 * self._anim_speed):
            self._cur_texture += self._update_direction
            self._last_text_update = 0
            if self._cur_texture >= len(self._idle_textures) - 1:
                self._update_direction = -1
            elif self._cur_texture <= 0:
                self._update_direction = 1
            self.texture = self._idle_textures[self._cur_texture]
        self._last_text_update += delta_time
        if self._anim_timer <= 0:
            self._anim_speed = 1
            self._anim_timer = 0
        else:
            self._anim_timer -= delta_time
            
    
    def _attack_animation(self):
        self._anim_speed = 8
        self._anim_timer = 3
    
    def attack(self):
        self._attack_animation()
        return randint(round(self._base_attack / 2), self._base_attack)
    
    def defend(self):
        return randint(round(self._base_defense / 2), self._base_defense)
    
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
