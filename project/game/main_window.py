import arcade
from game.overworld import Overworld
from game.battle import Battle
from game.inventory import Inventory

class MainWindow(arcade.Window):
    """
    Main application class.

    Stereotype: Controller, Interfacer
    """

    def __init__(self, width, height, title):
        """ Class Constructor

            Args:
                self (MainWindow): An instance of MainWindow
                width (int): The width of the main window
                height (int): The wight of the main window
                title (str): The title to show on the main window
        """
        super().__init__(width, height, title, resizable=True)

    def setup(self):
        """ Set up the game variables. Call to re-start the game.

            Args:
                self (MainWindow): An instance of MainWindow
        """
        self.set_mouse_visible(False)
        self.set_min_size(160, 144)
        self._overworld = Overworld()
        self._last_view = self._overworld
        self.battle = Battle()
        test_inventory = Inventory({'Yeet': 3, 'Bruh': 10, 'Brufh': 10, 'Bruhh': 10, 'Brduh': 10, 'BEruh': 10, 'Bruasdh': 10, 'Brdsuh': 10, 'Brfsuh': 10, 'Brufasdh': 10, 'Brfsuh': 10, 'Bafsrafsddsaasddfasdfsdfasasdfadsfdfsasdfasdfasdfdsfasdfadfsafdsdfasadfsadfsdasfadsfadfsasdfadsfadfsadsfasdfadsfssssssssssssssssssssssssssssssffffffffffffffffffffffffffffffffffffffffffffffffffuh': 10, 'Bruh': 10})
        self.show_view(self._overworld)


    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key in (arcade.key.F11, arcade.key.P):
            self.set_fullscreen(not self.fullscreen)

    def show_view(self, new_view):
        self._last_view = self.current_view
        super().show_view(new_view)

    @property
    def overworld(self):
        return self._overworld

    @property
    def last_view(self):
        return self._last_view
