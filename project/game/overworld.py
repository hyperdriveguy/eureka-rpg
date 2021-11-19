import arcade
import random
from game import constants
from game.player import Player
from pyglet.math import Vec2
from game.utils import is_between

class Overworld(arcade.View):


    def __init__(self):
        super().__init__()

        self.movement_lock = False

        self._left_pressed = False
        self._right_pressed = False
        self._up_pressed = False
        self._down_pressed = False

        self.free_camera = False
        self.free_coords = 0, 0

        # Keep track of the score
        self.show_score = False
        arcade.enable_timings()

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")

        arcade.set_background_color(arcade.color.GRAY)

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.setup()

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """

        # Setup the Camera
        self.camera = arcade.Camera(self.window.width, self.window.height)

        # Setup the GUI Camera
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        # Name of map file to load
        map_name = "project/assets/test_map.json"
        #map_name = f":resources:tiled_maps/map2_level_{self.level}.json"


        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
            "Coins": {
                "use_spatial_hash": True,
            },
            "Don't Touch": {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, constants.TILE_SCALING, layer_options)

        self.full_map_width = self.tile_map.width * self.tile_map.tile_width * self.tile_map.scaling
        self.full_map_height = self.tile_map.height * self.tile_map.tile_height * self.tile_map.scaling
        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Create the Sprite lists
        self.scene.add_sprite_list("Player")

        # Add Player Spritelist before "Foreground" layer. This will make the foreground
        # be drawn after the player, making it appear to be in front of the Player.
        # Setting before using scene.add_sprite allows us to define where the SpriteList
        # will be in the draw order. If we just use add_sprite, it will be appended to the
        # end of the order.
        self.scene.add_sprite_list_before("Player", 'Foreground')

        # Set up the player, specifically placing it at these coordinates.
        # image_source = ":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png"
        #image_source = 'project/assets/placeholder.png'
        self.player_sprite = Player()#arcade.Sprite(image_source, constants.CHARACTER_SCALING)
        self.player_sprite.center_x = constants.PLAYER_START_X
        self.player_sprite.center_y = constants.PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)

        # Update the players animation
        arcade.schedule(self.scene.update_animation, 1/40)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=0, walls=self.scene['Platforms']
        )

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = self.tile_map.width * 64 #GRID_PIXEL_SIZE

        self.yeet_layer = self.tile_map.object_lists["Object Layer 1"]

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below

        # Activate our Camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()

        if self.show_score:
            # Activate the GUI camera before drawing GUI elements
            self.gui_camera.use()

            # Draw player coordinates screen, scrolling it with the viewport
            coords = f"{self.player_sprite.center_x:.0f}, {self.player_sprite.center_y:.0f}"
            arcade.draw_text(
                coords,
                10,
                10,
                arcade.csscolor.WHITE,
                18,
            )

            try:
                arcade.draw_text(
                    f'{arcade.get_fps():.2f} FPS',
                    10,
                    10,
                    arcade.color.WHITE,
                    12,
                    self.gui_camera.viewport_width - 20,
                    'right'
                )
            except ValueError:
                print('Warning: Timings are not enabled.')

        for box in self.yeet_layer:
            try:
                text = box.properties["text"]
                if self._can_interact(box.shape):
                    arcade.draw_text(
                        text,
                        10,
                        50,
                        arcade.csscolor.WHITE,
                        18,
                    )
            except KeyError:
                print('Warning: Interactable has no assigned text.')

    def _can_interact(self, shape):
        begin_x = round(shape[0][0] * constants.TILE_SCALING)
        end_x = round(shape[1][0] * constants.TILE_SCALING)
        end_y = round(shape[0][1] * constants.TILE_SCALING) + self.full_map_height
        begin_y = round(shape[2][1] * constants.TILE_SCALING) + self.full_map_height
        if (is_between(self.player_sprite.center_x, begin_x, end_x) and
                is_between(self.player_sprite.center_y, begin_y, end_y)):
            return True
        return False

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        # Don't let camera travel past map
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        if screen_center_x > self.full_map_width - self.camera.viewport_width: 
            screen_center_x = self.full_map_width - self.camera.viewport_width
        if screen_center_y > self.full_map_height - self.camera.viewport_height:
            screen_center_y = self.full_map_height - self.camera.viewport_height
        player_centered = [screen_center_x, screen_center_y]
        self.free_coords = player_centered

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        if not self.movement_lock:
            if self._up_pressed and not self._down_pressed:
                self.player_sprite.change_y = constants.PLAYER_MOVEMENT_SPEED
            elif self._down_pressed and not self._up_pressed:
                self.player_sprite.change_y = -constants.PLAYER_MOVEMENT_SPEED
            else:
                self.player_sprite.change_y = 0

            if self._left_pressed and not self._right_pressed:
                self.player_sprite.change_x = -constants.PLAYER_MOVEMENT_SPEED
            elif self._right_pressed and not self._left_pressed:
                self.player_sprite.change_x = constants.PLAYER_MOVEMENT_SPEED
            else:
                self.player_sprite.change_x = 0

        # Move the player with the physics engine
        self.physics_engine.update()

        # Position the camera
        if not self.free_camera:
            self.center_camera_to_player()

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Add one to the score
            self.score += 1

        # See if the user got to the end of the level
        if self.player_sprite.center_x >= self.end_of_map:
            # Advance to the next level
            self.level += 1

            # Load the next level
            self.setup()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """

        if key == arcade.key.UP or key == arcade.key.W:
            self._up_pressed = True
        if key == arcade.key.DOWN or key == arcade.key.S:
            self._down_pressed = True
        if key == arcade.key.LEFT or key == arcade.key.A:
            self._left_pressed = True
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self._right_pressed = True

        if key == arcade.key.SPACE:
            arcade.play_sound(self.jump_sound)

        if key == arcade.key.RCTRL:
            if self.show_score:
                self.show_score = False
            else:
                self.show_score = True

        if key == arcade.key.Z:
            if self.free_camera:
                self.free_camera = False
            else:
                self.free_camera = True

        if key == arcade.key.M:
            if self.movement_lock:
                self.movement_lock = False
            else:
                self.movement_lock = True

        if self.free_camera:
            if key == arcade.key.T:
                self.camera.shake(Vec2(10,10))
            
            if key == arcade.key.L:
                self.free_coords[0] += 64
                self.camera.move_to(self.free_coords)

            if key == arcade.key.K:
                self.free_coords[1] -= 64
                self.camera.move_to(self.free_coords)
                
            if key == arcade.key.J:
                self.free_coords[0] -= 64
                self.camera.move_to(self.free_coords)
                
            if key == arcade.key.I:
                self.free_coords[1] += 64
                self.camera.move_to(self.free_coords)

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """

        if key == arcade.key.UP or key == arcade.key.W:
            self._up_pressed = False
        if key == arcade.key.DOWN or key == arcade.key.S:
            self._down_pressed = False
        if key == arcade.key.LEFT or key == arcade.key.A:
            self._left_pressed = False
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self._right_pressed = False

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

