"""Contains classes for the player battling.
"""
from game.contestant import Contestant

class BattlePlayer(Contestant):
    """Class used for the player during battle.

    Inherits: Contestant

    Stereotype: Information Holder
    """

    def __init__(self):
        """Initialize the contestant and other attributes.
        """
        super().__init__(['project/assets/battle_player.png',
                          'project/assets/battle_player_1.png',
                          'project/assets/battle_player_2.png'])
