"""Contains classes for the player battling.
"""
from game.contestant import Contestant
from game.constants import CONTESTANTS

class BattlePlayer(Contestant):
    """Class used for the player during battle.

    Inherits: Contestant

    Stereotype: Information Holder
    """

    def __init__(self):
        """Initialize the contestant and other attributes.
        """
        super().__init__(CONTESTANTS['player']['anim'], stat_dict=CONTESTANTS['player']['stats'])
