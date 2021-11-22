import arcade
from game import constants

class OverworldMap:

    def __init__(self, map_file, player):
        # Create the Sprite lists
        self._player = player

        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            "Foreground": {
                "use_spatial_hash": True,
            },
            "Walls": {
                "use_spatial_hash": True,
            },
            "Background": {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled map
        self._tile_map = arcade.load_tilemap(map_file, constants.TILE_SCALING, layer_options)

        # Calculate full map width and height
        self._full_map_width = self._tile_map.width * self._tile_map.tile_width * self._tile_map.scaling
        self._full_map_height = self._tile_map.height * self._tile_map.tile_height * self._tile_map.scaling

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self._scene = arcade.Scene.from_tilemap(self._tile_map)

        self._scene.add_sprite_list_before("Player", 'Foreground')
        self._scene.add_sprite("Player", self._player)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=0, walls=self.scene['Walls']
        )

        self.yeet_layer = self.tile_map.object_lists["Text"]
        