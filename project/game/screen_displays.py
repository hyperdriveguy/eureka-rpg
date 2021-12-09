import arcade
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class ScreenDisplay(arcade.View):
    """ Screen can be shown for the end of the game or while loading.

    Inherits: arcade.View

    Stereotype: Information Holder

    Attributes:
        self._text (str): the text to be written in the text display.
        self._text_display (arcade.Text): an instnace of acrade.Text. The text to display.
    """
    def __init__(self, text):
        """ Class Constructor
        """
        super().__init__()
        self._text = text
        self._text_display = arcade.Text(
            self._text,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.csscolor.WHITE,
            48,
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
        self._text_display.draw()
