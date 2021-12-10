import arcade
from game.utils import px_to_pt

class ScreenDisplay(arcade.View):
    """ Screen can be shown for the end of the game or while loading.

    Inherits: arcade.View

    Stereotype: Information Holder

    Attributes:
        self._text (str): the text to be written in the text display.
        self._text_display (arcade.Text): an instnace of acrade.Text. The text to display.
        self._next_view (arcade.View): view to switch to after this one.
    """
    def __init__(self, text, next_view):
        """ Class Constructor
        """
        super().__init__()
        self._next_view = next_view
        self._text = text
        self.on_resize(self.window.width, self.window.height)

    def on_show(self):
        """ Called when switching to this view
        """
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Draw the intro screen
        """
        arcade.start_render()
        self._text_display.draw()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            self.window.show_view(self._next_view)

    def on_resize(self, width, height):
        self._text_display = arcade.Text(
            self._text,
            width / 2,
            height / 2,
            arcade.csscolor.WHITE,
            px_to_pt(width / 12.5),
            anchor_x="center",
            anchor_y="center",
            width=width * 0.8
        )

