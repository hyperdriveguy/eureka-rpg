import arcade
from game.overworld_map import OverworldMap
from game.constants import TILE_SCALING

class MapSwitcher:

    def __init__(self, player, maps: dict):
        self._all_maps = maps
        self._player = player
        self._cur_map = None
        self.switch_map(next(iter(self._all_maps)))

    def switch_map(self, map_name, spawn=None):
        self._cur_map = OverworldMap(self._all_maps[map_name], self._player)
    
    def warp_map(self, warp_properties):
        map_name, warp_x, warp_y = warp_properties.split(',')
        map_name = map_name.strip()
        self.switch_map(map_name)
        warp_x = float(warp_x.strip()) * TILE_SCALING
        warp_y = (-float(warp_y.strip()) * TILE_SCALING) + self._cur_map.map_height
        self._player.center_x = warp_x
        self._player.center_y = warp_y
        print(type(warp_x), type(warp_y))
        print((warp_x), (warp_y))
        print(warp_properties)
        print(self._cur_map.map_height)
    
    @property
    def cur_map(self):
        return self._cur_map
    
    @cur_map.setter
    def cur_map(self, cur_map):
        self.switch_map(cur_map)
