""" The map switcher"""
from game.overworld_map import OverworldMap
from game.constants import TILE_SCALING

class MapSwitcher:
    """ Logic to switch between maps

    Stereotype: Information Holder, Controller

    Attributes:
        self._all_maps (dict): the maps that can be used
        self._player: The player sprite
        self._cur_map: the current map
    """
    def __init__(self, player, maps: dict):
        """ Class Constructor

        Args:
            player (sprite): The player
            maps (dict): The dictionary of maps
        """
        self._all_maps = maps
        self._player = player
        self._cur_map = None
        self._cur_map_name = ''
        self.switch_map(next(iter(self._all_maps)))

    def switch_map(self, map_name):
        """ Switch to another overworld map

        Args:
            map_name (str): the name of the map
            spawn ([type], optional): [description]. Defaults to None.
        """
        self._cur_map_name = map_name
        self._cur_map = OverworldMap(self._all_maps[map_name], self._player)

    def warp_map(self, warp_properties: str):
        """ Warp to another map

        Args:
            warp_properties (str): the warp destination
        """
        map_name, warp_x, warp_y = warp_properties.split(',')
        map_name = map_name.strip()
        # Don't reload the map if the warp is on the same map
        if map_name != self._cur_map_name:
            print('reloading map')
            self.switch_map(map_name)
        warp_x = float(warp_x.strip()) * TILE_SCALING
        warp_y = (-float(warp_y.strip()) * TILE_SCALING) + self._cur_map.map_height
        self._player.center_x = warp_x
        self._player.center_y = warp_y

    @property
    def cur_map(self):
        """ Get the current map

        Returns:
            map: The current map
        """
        return self._cur_map

    @cur_map.setter
    def cur_map(self, cur_map):
        """ Set the current map

        Args:
            cur_map ([type]): The current map
        """
        self.switch_map(cur_map)
