""" The Overworld Map """
from concurrent.futures import ThreadPoolExecutor
import arcade
from game import constants
from game.interactable import Interactable

class OverworldMap:
    """ Responsible for the map
    Stereotype: Information Holder, Controller

    Attributes:
        self._player = player
        layer_options (dict): set some layer options to use spatial hashing

        self._tile_map: tiled map

        # Calculate full map width and height
        self._full_map_width (int):The width of the map
        self._full_map_height (int):The height of the map
    """
    def __init__(self, map_file, player, spawn=None):
        """ Class Constructor

        Args:
            map_file (file): map file
            player (sprite): player sprite
            spawn ([type], optional): [description]. Defaults to None.
        """
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

        self._background_music = arcade.load_sound(":resources:sounds/jump1.wav") #Change this
        self._play_background_music = arcade.play_sound(self._background_music, looping=True)

        # Read in the tiled map
        self._tile_map = arcade.load_tilemap(constants.MAP_PATH + map_file, constants.TILE_SCALING, layer_options)

        # Calculate full map width and height
        self._full_map_width = self._tile_map.width * self._tile_map.tile_width * self._tile_map.scaling
        self._full_map_height = self._tile_map.height * self._tile_map.tile_height * self._tile_map.scaling

        if spawn is None:
            self._spawn = self._tile_map.object_lists['Spawn'][0]
            self._player.center_x, self._player.center_y = self._spawn.shape
        else:
            self._player.center_x, self._player.center_y = spawn
        
        def build_map_objects():
            """ Build the interactable map objects"""
            self._text_objects = Interactable(self._tile_map.object_lists['Text'], self._player, self._full_map_height)

        def build_map_scene():
            """ Initialize Scene with our TileMap, this will automatically add all layers
             from the map as SpriteLists in the scene in the proper order."""
            self._scene = arcade.Scene.from_tilemap(self._tile_map)

            self._scene.add_sprite_list_before("Player", 'Foreground')
            self._scene.add_sprite("Player", self._player)

            # Create the 'physics engine'
            self._physics_engine = arcade.PhysicsEnginePlatformer(
                self._player, gravity_constant=0, walls=self._scene['Walls']
            )

        with ThreadPoolExecutor() as threader:
            threader.submit(build_map_objects)
            threader.submit(build_map_scene)


    def draw(self):
        """Draw the Scene"""
        self._scene.draw()

    def update(self, delta_time):
        """ Update physics engine, player animation, and interactable object

        Args:
            delta_time (float): time in seconds since method was last called.
        """
        # Move the player with the physics engine
        self._physics_engine.update()

        # Update the players animation
        self._scene.update_animation(delta_time)

        # Update interactable objects
        self._text_objects.update_interactable(delta_time)

    def on_keypress(self, key, key_modifiers):
        """Called whenever a key on the keyboard is pressed.

        Args:
            key (int): key that was pressed.
            key_modifiers (int): key modifier that was pressed.
        """
        self._text_objects.update_interactable(force_check=True)

    @property
    def map_width(self):
        """ Get the full width of the map

        Returns:
            int: full map width
        """
        return self._full_map_width

    @property
    def map_height(self):
        """ Get the full height of the map

        Returns:
            int: full map height
        """
        return self._full_map_height

    @property
    def map_scene(self):
        """ Get the tilemap scene

        Returns:
            arcade.Scene: the scene which was built with tilemap
        """
        return self._scene

    @property
    def player_can_interact(self):
        """ Get player_can_interact

        Returns:
            bool: player can interact
        """
        return self._text_objects.can_interact

    @property
    def object_text(self):
        """ Get the object text

        Returns:
            str: the object's text
        """
        return self._text_objects.interact_text

    @property
    def object_properties(self):
        """Get the dictionary of objects in the map

        Returns:
            dict: dictionary of map object properties
        """
        return self._text_objects.interact_properties
