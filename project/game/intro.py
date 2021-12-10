import arcade
from game.constants import GAME_NAME
from game.utils import px_to_pt

class IntroView(arcade.View):
    """ Splash screen for the game. Press spacebar to start game

    Inherits: arcade.View

    Stereotype: Controller

    Attributes:
        self._game_name (arcade.Text): an instnace of arcade.Text. Displays the game name.
        self._start_game (arcade.Text): an instnace of arcade.Text. Display how to start the game.
    """
    def __init__(self):
        """ Class Constructor
        """
        super().__init__()
        self.on_resize(self.window.width, self.window.height)


    def on_show(self):
        """ Called when switching to this view
        """
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Draw the intro screen
        """
        arcade.start_render()
        self._game_name.draw()
        self._start_game.draw()

    def on_key_press(self, key, key_modfiers):
        """Called whenever a key on the keyboard is pressed.

        Args:
            key (int): key that was pressed.
            key_modifiers (int): key modifier that was pressed.
        """
        if key == arcade.key.SPACE:
            self.window.overworld.setup()
            self.window.show_view(self.window.overworld)

    def on_resize(self, width, height):
        self._game_name = arcade.Text(
            GAME_NAME,
            width / 2,
            height / 2 + width / 12.5,
            arcade.csscolor.WHITE,
            px_to_pt(width / 12.5),
            anchor_x="center",
            anchor_y="center"
        )
        self._start_game = arcade.Text(
            "press SPACE to begin",
            width / 2,
            height / 2 - width / 25,
            arcade.csscolor.WHITE,
            px_to_pt(width / 25),
            anchor_x="center",
            anchor_y="center"
        )

