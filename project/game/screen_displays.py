"""This module includes transition splash that are configurable.
"""
import arcade
from game.utils import px_to_pt

class SplashView(arcade.View):
    """Screen can be shown for the end of the game or while loading.

    Inherits: arcade.View

    Stereotype: Information Holder

    Attributes:
        self._text (str): the text to be written in the text display.
        self._text_display (arcade.Text): an instnace of acrade.Text. The text to display.
        self._next_view (arcade.View): view to switch to after this one.
    """
    def __init__(self, text, next_view, cont_msg=True):
        """Class Constructor
        """
        super().__init__()
        self._next_view = next_view
        self._text = text
        self._cont_msg = cont_msg
        self._long_msg = len(text) > 20
        self.on_resize(self.window.width, self.window.height)

    def on_show(self):
        """Called when switching to this view
        """
        self.on_resize(self.window.width, self.window.height)
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Draw the intro screen
        """
        arcade.start_render()
        self._screen_msg.draw()
        if self._cont_msg:
            self._continue_msg.draw()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            self.window.show_view(self._next_view)

    def on_resize(self, width, height):
        if self._long_msg:
            self._screen_msg = arcade.Text(
                self._text,
                width / 2,
                height / 2 + width / 30,
                arcade.csscolor.WHITE,
                px_to_pt(width / 30),
                anchor_x="center",
                anchor_y="center",
                width=width * 0.8
            )
        else:
            self._screen_msg = arcade.Text(
                self._text,
                width / 2,
                height / 2 + width / 20,
                arcade.csscolor.WHITE,
                px_to_pt(width / 20),
                anchor_x="center",
                anchor_y="center",
                width=width * 0.8
            )
        if self._cont_msg:
            self._continue_msg = arcade.Text(
                "press SPACE to continue",
                width / 2,
                height / 2 - width / 35,
                arcade.csscolor.WHITE,
                px_to_pt(width / 35),
                anchor_x="center",
                anchor_y="center",
                width=width * 0.8
            )
