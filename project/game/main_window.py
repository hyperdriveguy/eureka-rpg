""" The Main Window """
import arcade
from game.overworld import Overworld
from game.screen_displays import SplashView
from game.intro import IntroView


class MainWindow(arcade.Window):
    """
    Main application class.

    Inherits: arcade.Window

    Stereotype: Controller, Interfacer

    Attributes:
        self.show_debug (bool): Check if debugging info should be shown
    """

    def __init__(self, width, height, title):
        """ Class Constructor

            Args:
                self (MainWindow): An instance of MainWindow
                width (int): The width of the main window
                height (int): The height of the main window
                title (str): The title to show on the main window
        """
        super().__init__(width, height, title, resizable=True)
        self._intro = IntroView()
        self._end = SplashView("You Win!", self._intro)
        self._you_died = SplashView("You Died", self._intro)
        self._win_game = SplashView("You Won the Game!", self._intro)
        self._game_over = SplashView("Game Over", self._intro)
        self._overworld = Overworld()
        self._win_battle = SplashView("The enemy has been defeated", self._overworld)
        self._lose_battle = SplashView("You lost the battle", self._overworld)
        self._last_view = self._overworld

        self.show_debug = False
        arcade.enable_timings()

    def setup(self):
        """
        Set up the game variables. Call to re-start the game.
        """
        self.set_mouse_visible(False)
        self.set_min_size(370, 260)
        self.show_view(self._intro)

        # Setup the debug info Camera
        self._debug_info_cam = arcade.Camera(self.width, self.height)
        # self.show_view(self._overworld)
        # self.show_view(self._end)

    def _draw_debug_display(self):
        if self.show_debug:
            # Activate the GUI camera before drawing GUI elements
            self._debug_info_cam.use()
        
            # Draw player coordinates screen, scrolling it with the viewport
            try:
                coords = (f'{self._overworld.player_sprite.center_x:.0f}, '
                        f'{self._overworld.player_sprite.center_y:.0f}, '
                        f'{self._overworld.player_sprite.character_face_direction}')
                arcade.draw_text(
                    coords,
                    10,
                    10,
                    arcade.csscolor.WHITE,
                    18,
                )
            except AttributeError:
                print('Overworld player sprite not initialized, skipping debug data')
            
            try:
                if self._overworld._active_textbox:
                    textbox_debug_info = (f'cur_text length: {len(self._overworld.cur_text)}, '
                                        f'number of lines: {self._overworld._text_box.num_lines}')
                    arcade.draw_text(
                        textbox_debug_info,
                        10,
                        50,
                        arcade.csscolor.WHITE,
                        18
                    )
            except AttributeError:
                print('Textbox not initialized but showing active, continuing')
            try:
                cur_fps = arcade.get_fps()
                if cur_fps >= 60:
                    fps_color = arcade.color.GREEN
                elif cur_fps >= 45:
                    fps_color = arcade.color.YELLOW
                elif cur_fps >= 30:
                    fps_color = arcade.color.ORANGE
                else:
                    fps_color = arcade.color.RED
                arcade.draw_text(
                    f'{cur_fps:.2f} FPS',
                    10,
                    10,
                    fps_color,
                    12,
                    self._debug_info_cam.viewport_width - 20,
                    'right'
                )
            except ValueError:
                print('Warning: Timings are not enabled.')

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        Args:
            key (int): key that was pressed.
            key_modifiers (int): key modifier that was pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key in (arcade.key.F11, arcade.key.P):
            self.set_fullscreen(not self.fullscreen)

        if key in (arcade.key.RCTRL, arcade.key.RCOMMAND):
            self.show_debug = not self.show_debug

    def on_draw(self):
        self._draw_debug_display()

    def show_view(self, new_view):
        """ Show the desired view.

        Args:
            new_view (arcade.View): An instance of acrade.View
        """
        self._last_view = self.current_view
        super().show_view(new_view)

    def on_resize(self, width: int, height: int):
        """ Resize camera and gui_camera

            Args:
                self (Overworld): An instance of Overworld
                width (int): The width of the camera size
                height (int): The height of the camera size
        """
        self._debug_info_cam.resize(width, height)

    @property
    def overworld(self):
        """ Get overworld

        Returns:
            Overworld: An instance of Overworld
        """
        return self._overworld

    @property
    def death_screen(self):
        """ Get overworld

        Returns:
            Overworld: An instance of Overworld
        """
        return self._you_died

    @property
    def last_view(self):
        """ Get last_view

        Returns:
            Overworld: self._overworld - an instance of Overworld
        """
        return self._last_view
