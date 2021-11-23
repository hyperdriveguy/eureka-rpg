import arcade
import random

from game import constants
from game.player import Player
from game.overworld_map import OverworldMap
from pyglet.math import Vec2


class Overworld(arcade.View):
    """Contains functions exclusive to the overworld.

    Stereotype: Controller, Information Holder, Interfacer
    """


    def __init__(self):
        super().__init__()

        self._active_textbox = False

        self.cur_text = 'asdf'

        self.free_camera = False
        self.free_coords = 0, 0

        # Keep track of the score
        self.show_debug = False
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

        # Add Player Spritelist before "Foreground" layer. This will make the foreground
        # be drawn after the player, making it appear to be in front of the Player.
        # Setting before using scene.add_sprite allows us to define where the SpriteList
        # will be in the draw order. If we just use add_sprite, it will be appended to the
        # end of the order.

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = Player()
        self.player_sprite.center_x = constants.PLAYER_START_X
        self.player_sprite.center_y = constants.PLAYER_START_Y

        # Init map
        map_name = "project/assets/test_map.json"
        self._cur_map = OverworldMap(map_name, self.player_sprite)


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

        self._cur_map.draw()

        if self._active_textbox:
            self.gui_camera.use()
            arcade.draw_text(
                self.cur_text,
                10,
                50,
                arcade.csscolor.WHITE,
                18
            )
        

        if self.show_debug:
            # Activate the GUI camera before drawing GUI elements
            self.gui_camera.use()

            # Draw player coordinates screen, scrolling it with the viewport
            coords = f"{self.player_sprite.center_x:.0f}, {self.player_sprite.center_y:.0f}, {self.player_sprite.character_face_direction}"
            arcade.draw_text(
                coords,
                10,
                10,
                arcade.csscolor.WHITE,
                18,
            )

            try:
                cur_fps = arcade.get_fps()
                if cur_fps >= 60:
                    fps_color = arcade.color.GREEN
                elif cur_fps >= 45 and cur_fps < 60:
                    fps_color = arcade.color.YELLOW
                elif cur_fps >= 30 and cur_fps < 45:
                    fps_color = arcade.color.ORANGE
                else:
                    fps_color = arcade.color.RED
                arcade.draw_text(
                    f'{cur_fps:.2f} FPS',
                    10,
                    10,
                    fps_color,
                    12,
                    self.gui_camera.viewport_width - 20,
                    'right'
                )
            except ValueError:
                print('Warning: Timings are not enabled.')

    def center_camera(self, sprite: arcade.Sprite):
        screen_center_x = sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = sprite.center_y - (self.camera.viewport_height / 2)

        # Don't let camera travel past map
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        if screen_center_x > self._cur_map.map_width - self.camera.viewport_width: 
            screen_center_x = self._cur_map.map_width - self.camera.viewport_width
        if screen_center_y > self._cur_map.map_height - self.camera.viewport_height:
            screen_center_y = self._cur_map.map_height - self.camera.viewport_height
        player_centered = [screen_center_x, screen_center_y]
        self.free_coords = player_centered

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        # Update player movement
        self.player_sprite.on_update(delta_time)

        # Update current map
        self._cur_map.update(delta_time)

        # Position the camera
        if not self.free_camera:
            self.center_camera(self.player_sprite)
        
        if not self._active_textbox:
            if self._cur_map.player_can_interact:
                self.player_sprite.color = arcade.color.RED
            else:
                self.player_sprite.color = arcade.color.WHITE
        else:
            self.player_sprite.color = arcade.color.WHITE

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        # Get player movements
        self.player_sprite.on_key_press(key, key_modifiers)

        if key == arcade.key.RCTRL or key == arcade.key.RCOMMAND:
            if self.show_debug:
                self.show_debug = False
            else:
                self.show_debug = True

        if key == arcade.key.Z:
            if self.free_camera:
                self.free_camera = False
            else:
                self.free_camera = True

        if key == arcade.key.M:
            if self.player_sprite.allow_player_input:
                self.player_sprite.allow_player_input = False
            else:
                self.player_sprite.allow_player_input = True

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
        # Stop player movments
        self.player_sprite.on_key_release(key, key_modifiers)
        
        if not self._active_textbox:
            try:
                if self._cur_map.player_can_interact:
                    if key == arcade.key.SPACE:
                        arcade.play_sound(self.jump_sound)
                        self.cur_text = self._cur_map.object_text
                        self._active_textbox = True
                        self.player_sprite.force_movement_stop()

            except KeyError:
                print('Warning: Interactable has no assigned text.')
        else:
            if key == arcade.key.SPACE:
                arcade.play_sound(self.jump_sound)
                self._active_textbox = False
                self.player_sprite.allow_player_input = True
