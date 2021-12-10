""" The Player """
from game.battle_player import BattlePlayer
from game.overworld_player import OverworldPlayer


class Player:
    """ Various views

    Attributes:
        self._overworld (OverworldPlayer): an instance of OverworldPlayer
        self._battle (BattlePlayer): an instnace of BattlePlayer
        self._inventory (dict): dictionary of inventory
    """
    def __init__(self):
        """ Class contstructor
        """
        self._overworld = OverworldPlayer()
        self._battle = BattlePlayer()
        self._inventory = {'Yeet': 3, 'Bruh': 10}
