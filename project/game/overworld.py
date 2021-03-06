""" The Overworld """
import arcade

from game import constants
from game.battle import Battle
from game.map_switcher import MapSwitcher
from game.overworld_player import OverworldPlayer
from game.text_box import DrawTextBox
from game.save import Save


class Overworld(arcade.View):
    """Contains functions exclusive to the overworld.

    Inherits: arcade.View

    Stereotype: Controller, Information Holder, Interfacer

    Attributes:
        self._active_textbox (bool): Check if textbox is activated

        self.cur_text (str): the current text to be displayed

        self.free_camera (bool): Check if camera should be changed to free mode
        self.free_coords (): coordinates of the free camera

        self.collect_coin_sound (): sound of collecting coins
        self.jump_sound (): sound of jump
        self.game_over (): sound of gameover
    """
    def __init__(self):
        """ Class Constructor """
        super().__init__()

        self._active_textbox = False

        self.cur_text = ''

        self.free_camera = False
        self.free_coords = 0, 0

        self._text_box = None
        self._cur_battle = None

        self._save_battle = Save(constants.SAVE_BATTLE_PATH)
        self._save_battle.clear_file()

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")

        arcade.set_background_color(arcade.color.GRAY)

        # If you have sprite lists, you should create them here,
        # and set them to None
        # self.setup()

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
        self.player_sprite = OverworldPlayer()
        self.player_sprite.center_x = constants.PLAYER_START_X
        self.player_sprite.center_y = constants.PLAYER_START_Y

        # Init Maps
        self._map_switcher = MapSwitcher(self.player_sprite, constants.MAPS)

    def on_show_view(self):
        weeping_cowboy = arcade.load_sound("project/assets/sounds/weeping_cowboy.wav")
        self._background_music = arcade.play_sound(weeping_cowboy, looping=True)

    def on_hide_view(self):
        arcade.stop_sound(self._background_music)

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
        self._map_switcher.cur_map.draw()

        if self._active_textbox:
            self.gui_camera.use()
            self._text_box.draw()

    def center_camera(self, sprite: arcade.Sprite):
        """ Center the camera on the player

        Args:
            sprite (arcade.Sprite): The sprite to center the camera around
        """
        screen_center_x = sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = sprite.center_y - (self.camera.viewport_height / 2)

        # Don't let camera travel past map
        screen_center_x = max(screen_center_x, 0)
        screen_center_y = max(screen_center_y, 0)
        if screen_center_x > self._map_switcher.cur_map.map_width - self.camera.viewport_width:
            screen_center_x = self._map_switcher.cur_map.map_width - self.camera.viewport_width
        if screen_center_y > self._map_switcher.cur_map.map_height - self.camera.viewport_height:
            screen_center_y = self._map_switcher.cur_map.map_height - self.camera.viewport_height
        player_centered = [screen_center_x, screen_center_y]
        self.free_coords = player_centered

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """ All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.

        Args:
            delta_time (float): time in seconds since method was last called.
        """
        # Update player movement
        self.player_sprite.on_update(delta_time)

        # Update current map
        self._map_switcher.cur_map.update(delta_time)

        # Position the camera
        if not self.free_camera:
            self.center_camera(self.player_sprite)

        if not self._active_textbox and self._map_switcher.cur_map.player_can_interact:
            self.player_sprite.player_highlighted = True
        else:
            self.player_sprite.player_highlighted = False

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        Args:
            key (int): key that was pressed.
            key_modifiers (int): key modifier that was pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        # Get player movements
        self.player_sprite.on_key_press(key, key_modifiers)

        self._map_switcher.cur_map.on_keypress(key, key_modifiers)

        if not self._active_textbox:
            try:
                if self._map_switcher.cur_map.player_can_interact and key == arcade.key.SPACE:
                    self._do_interact()
            except KeyError:
                print('Warning: Interactable has no relevant properties.')
                print(self._map_switcher.cur_map.object_properties)
        elif key == arcade.key.SPACE:
            arcade.play_sound(self.jump_sound)
            if self._text_box.text_end:
                self._active_textbox = False
                self.player_sprite.allow_player_input = True
                if (self._map_switcher.cur_map.object_properties['type'].lower() == 'battle' and
                        not self._save_battle.battle_complete(
                            self._map_switcher.cur_map.object_properties['battle'])):
                    self.window.show_view(Battle(self._cur_battle))

            else:
                self._text_box.line_by_line()

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.

        Args:
            key (int): key that was pressed.
            key_modifiers (int): key modifier that was pressed.
        """
        # Stop player movments
        self.player_sprite.on_key_release(key, key_modifiers)

    def _do_interact(self):
        """ Interact with map
        """
        arcade.play_sound(self.jump_sound)
        if self._map_switcher.cur_map.object_properties['type'].lower() == 'text':
            self.cur_text = self._map_switcher.cur_map.object_text
        elif self._map_switcher.cur_map.object_properties['type'].lower() == 'battle':
            if self._save_battle.battle_complete(
                    self._map_switcher.cur_map.object_properties['battle']):
            # if self._map_switcher.cur_map.object_properties['battle'] in self.battles_won:
                self.cur_text = self._map_switcher.cur_map.object_properties['afterbattle']
            else:
                self.cur_text = self._map_switcher.cur_map.object_properties['prebattle']
                self._cur_battle = self._map_switcher.cur_map.object_properties['battle']
        if self._map_switcher.cur_map.object_properties['type'].lower() == 'warp':
            self._map_switcher.warp_map(self._map_switcher.cur_map.object_properties['warp'])
        else:
            self._active_textbox = True
            self._text_box = DrawTextBox(self.cur_text, self.window)
            self.player_sprite.force_movement_stop()

    def on_resize(self, width: int, height: int):
        """ Resize camera and gui_camera

            Args:
                self (Overworld): An instance of Overworld
                width (int): The width of the camera size
                height (int): The height of the camera size
        """
        self.camera.resize(width, height)
        self.gui_camera.resize(width, height)

        try:
            self._text_box.resize(width, height)
        except AttributeError:
            pass
