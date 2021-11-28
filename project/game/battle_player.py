import arcade
from game.contestant import Contestant

class BattlePlayer(Contestant):

    def __init__(self):
        super().__init__()
    
    def update_animation(self, delta_time: float = 1 / 60):
        pass