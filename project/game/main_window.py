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

    def setup(self):
        """
        Set up the game variables. Call to re-start the game.
        """
        self.set_mouse_visible(False)
        self.set_min_size(370, 260)
        self.show_view(self._intro)
        # self.show_view(self._overworld)
        # self.show_view(self._end)

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

    def show_view(self, new_view):
        """ Show the desired view.

        Args:
            new_view (arcade.View): An instance of acrade.View
        """
        self._last_view = self.current_view
        super().show_view(new_view)

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
