"""Contains classes for the player battling.
"""

import arcade
from game.contestant import Contestant


class BattlePlayer(Contestant):
    """Class used for the player during battle.

    Inherits: Contestant
    """

    def __init__(self):
        """Initialize the contestant and other attributes.
        """
        super().__init__(['project/assets/player_placeholder.png',
                          'project/assets/player_placeholder_2.png',
                          'project/assets/player_placeholder_3.png'])
