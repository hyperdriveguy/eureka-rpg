import arcade
from game.overworld import Overworld

class MainWindow(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        self.overworld = Overworld()
        self.show_view(self.overworld)


    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == arcade.key.F11:
            if not self.fullscreen:
                self.set_fullscreen(True)
                self.overworld.camera.resize(self.width, self.height)
            else:
                self.set_fullscreen(False)
                self.overworld.camera.resize(self.width, self.height)