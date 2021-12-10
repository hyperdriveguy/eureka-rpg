import arcade
from game.constants import GAME_NAME, SCREEN_WIDTH, SCREEN_HEIGHT

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
        
        self._game_name = arcade.Text(
            GAME_NAME,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 35,
            arcade.csscolor.WHITE,
            48,
            anchor_x="center",
            anchor_y="center"
        )
        self._start_game = arcade.Text(
            "press SPACE to begin",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 35,
            arcade.csscolor.WHITE,
            24,
            anchor_x="center",
            anchor_y="center"
        )

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
            self.window.show_view(self.window.overworld)
