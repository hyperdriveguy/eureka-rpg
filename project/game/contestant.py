"""Contains classes for battle contestants.
"""
from typing import Iterable
from random import randint
import arcade
from game import constants


class Contestant(arcade.Sprite):
    """A contestant in battle.

    Inherits: arcade.Sprite

    Stereotype: Information Holder

    Attributes:
        self._scale (int): scaling for characters
        self._is_turn (bool): determine if it is contestants turn

        self._base_heart_points (int): contestants max hp
        self._base_attack (int): contestants max attack capability
        self._base_defense (int): contestants max defense capability
        self._base_skill (int): contestants max skill level
        self._base_speed (int): contestants max speed capability

        self._cur_heart_points (int): contestants current hp
        self._attack_mod (int): attack modifier
        self._defense_mod (int): defense modifier
        self._skill_mod (int): skill modifier
        self._speed_mod (int): speed modifier

        self._last_text_update (int):
        self._cur_texture (int): the index of current texture to call from textures list
        self._update_direction (int): update contestant direction
        self._anim_speed (int): animation speed
        self._anim_timer (int): animation timer
        self._idle_textures (list): list of textures for animation
    """
    def __init__(self,
                 idle_pics: Iterable,
                 hp=10,
                 attack=5,
                 defense=5,
                 skill=5,
                 speed=5,
                 stat_dict: dict=None):
        """Initialize attributes of the contestant.

        Args:
            idle_pics (Iterable): list of images to use for the idle animation.
            hp (int, optional): Max HP. Defaults to 10.
            attack (int, optional): Max attack. Defaults to 5.
            defense (int, optional): Max defense. Defaults to 5.
            skill (int, optional): Max skill. Defaults to 5.
            speed (int, optional): Max speed. Defaults to 5.
        """
        super().__init__()
        self._scale = constants.CHARACTER_SCALING
        self._is_turn = False

        if stat_dict is None:
            # Base Battle Stats
            self._base_heart_points = hp
            self._base_attack = attack
            self._base_defense = defense
            self._base_skill = skill
            self._base_speed = speed
        else:
            self.all_stats = stat_dict

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
        """Update the contestant's animation.

        Args:
            delta_time (float): time in seconds since method was last called.
                Defaults to 1/60.
        """
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
        """Set flags for preforming an attack animation.
        """
        self._anim_speed = 8
        self._anim_timer = 3

    def attack(self):
        """Preform an attack based on attack stat.

        Returns:
            int: damage dealt.
        """
        self._attack_animation()
        return randint(round(self._base_attack / 2), self._base_attack)

    def defend(self):
        """Prevent damage based on defense stat.

        Returns:
            int: damage negated
        """
        return randint(round(self._base_defense / 2), self._base_defense)

    @property
    def is_turn(self):
        """Flag determining wether it is currently the player's turn.

        Returns:
            bool: player's turn
        """
        return self._is_turn

    @is_turn.setter
    def is_turn(self, is_turn: bool):
        """ Set is_turn

        Args:
            is_turn (bool): determine if it is the player's turn
        """
        self._is_turn = is_turn

    @property
    def cur_hp(self):
        """ Get current player HP.

        Returns:
            int: current HP
        """
        return self._cur_heart_points

    @cur_hp.setter
    def cur_hp(self, cur_hp: int):
        """ Set cur_hp

        Args:
            cur_hp (int): Current player HP
        """
        self._cur_heart_points = cur_hp

    @property
    def max_hp(self):
        """ Get Max player HP.

        Returns:
            int: max HP
        """
        return self._base_heart_points

    @property
    def all_stats(self):
        """ Get all contestant stats

        Returns:
            dictionary: contestant base stats
        """
        return {'HP': self._base_heart_points,
                'Attack': self._base_attack,
                'Defense': self._base_defense,
                'Skill': self._base_skill,
                'Speed': self._base_speed
                }

    @all_stats.setter
    def all_stats(self, all_stats: dict):
        """ Set contestant's base stats to a dictionary

        Args:
            all_stats (dict): dictionary of all the contestants base stats
        """
        self._base_heart_points = all_stats['HP']
        self._base_attack = all_stats['Attack']
        self._base_defense = all_stats['Defense']
        self._base_skill = all_stats['Skill']
        self._base_speed = all_stats['Speed']
