import arcade
from game.overworld_map import OverworldMap

class MapSwitcher:

    def __init__(self, player, maps: dict):
        self._all_maps = maps
        self._player = player
        self._cur_map = None
        self.switch_map(next(iter(self._all_maps)))

    def switch_map(self, map_name):
        self._cur_map = OverworldMap(self._all_maps[map_name], self._player)
    
    @property
    def cur_map(self):
        return self._cur_map
    
    @cur_map.setter
    def cur_map(self, cur_map):
        self.switch_map(cur_map)
