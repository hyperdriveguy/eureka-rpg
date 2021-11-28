import arcade
from game.contestant import Contestant

class BattlePlayer(Contestant):

    def __init__(self):
        super().__init__(['project/assets/player_placeholder.png', 'project/assets/player_placeholder_2.png', 'project/assets/player_placeholder_3.png'])
