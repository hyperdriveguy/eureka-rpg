"""Stores enemy data
"""

from game.constants import CONTESTANTS
from game.contestant import Contestant


class EnemySwitcher:
    """Logic to retrieve enemies easily.

    Stereotype: Information Holder, Controller

    Attributes:
        self._enemy_dict (dict): the enemies that can be used by maps for battling.
    """

    def __init__(self):
        """Class constructor.

        Parses constants to store contestants.
        """
        self._enemy_dict = {}
        for enemy, attrs in CONTESTANTS.items():
            enemy_contestant = Contestant(attrs['anim'], stat_dict=attrs['stats'])
            self._enemy_dict[enemy] = enemy_contestant

    def add(self, enemy_name: str, enemy: Contestant):
        """Add an enemy to be fetched later not in constants.

        Args:
            enemy_name (str): key for fetching the enemy later
            enemy (Contestant): contestant to battle
        """
        self._enemy_dict[enemy_name] = enemy

    def get(self, enemy_name) -> Contestant:
        """Fetch an enemy from the dictionary.

        Args:
            enemy_name (str): key associated with the enemy.

        Returns:
            Contestant: the contestant to fetch for battle.
        """
        return self._enemy_dict[enemy_name]
