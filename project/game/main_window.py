import arcade
from game.overworld import Overworld

class MainWindow(arcade.Window):
    """
    Main application class.

    Stereotype: Controller, Interfacer
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        self.set_mouse_visible(False)
        self.overworld = Overworld()
        self.show_view(self.overworld)


    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == arcade.key.F11 or key == arcade.key.P:
            if not self.fullscreen:
                self.set_fullscreen(True)
                
            else:
                self.set_fullscreen(False)
                