import arcade

from game.overworld_player import OverworldPlayer
from game.battle_player import BattlePlayer

class Player:

    def __init__(self):
        self._overworld = OverworldPlayer()
        self._battle = BattlePlayer()
        self._inventory = {}
