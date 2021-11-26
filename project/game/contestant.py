import arcade
from game import constants

class Contestant(arcade.Sprite):

    def __init__(self):
        self._scale = constants.CHARACTER_SCALING
        
        # Base Battle Stats
        self._heart_points = 10
        self._attack = 5
        self._defense = 5
        self._skill = 5
        self._speed = 5
    
    def update_animation(self, delta_time: float = 1 / 60):
        raise ValueError('"update_animation" was properly overridden by child.')
    

