import arcade
from game import constants
from game.interactable import Interactable

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
        self._physics_engine = arcade.PhysicsEnginePlatformer(
            self._player, gravity_constant=0, walls=self._scene['Walls']
        )

        self._spawn = self._tile_map.object_lists['Spawn']
        self._text_objects = Interactable(self._tile_map.object_lists['Text'], self._player, self._full_map_height)
    
    def draw(self):
        # Draw our Scene
        self._scene.draw()


    def update(self, delta_time):
        # Move the player with the physics engine
        self._physics_engine.update()

        # Update the players animation
        self._scene.update_animation(delta_time)

        # Update interactable objects
        self._text_objects.update_interactable(force_check=(delta_time >= 1/30))

    @property
    def map_width(self):
        return self._full_map_width

    @property
    def map_height(self):
        return self._full_map_height
    
    @property
    def map_scene(self):
        return self._scene
    
    @property
    def player_can_interact(self):
        return self._text_objects.can_interact
    
    @property
    def object_text(self):
        return self._text_objects.interact_text
