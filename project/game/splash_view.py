import arcade

class SplashView(arcade.View):
    """ Splash screen for the game. Press spacebar to start game

    Inherits: arcade.View

    Stereotype: Controller

    Attributes:
        self._game_name (arcade.Text): an instnace of arcade.Text. Displays the game name.
        self._start_game (arcade.Text): an instnace of arcade.Text. Display how to start the game.
    """
    def __init__(self, screen_msg, cont_msg=True, long_msg=False):
        """ Class Constructor
        """
        super().__init__()

        # self.on_resize(self.window.width, self.window.height)
        self._message = screen_msg
        self._cont_msg = cont_msg
        self._long_msg = long_msg
        if self._long_msg:
            self._screen_msg = arcade.Text(
                self._message,
                self.window.width / 2,
                self.window.height / 2 + self.window.width / 12.5,
                arcade.csscolor.WHITE,
                36,
                anchor_x="center",
                anchor_y="center"
            )
        else:
            self._screen_msg = arcade.Text(
                self._message,
                self.window.width / 2,
                self.window.height / 2 + self.window.width / 12.5,
                arcade.csscolor.WHITE,
                54,
                anchor_x="center",
                anchor_y="center"
            )
        if self._cont_msg:
            self._continue_msg = arcade.Text(
                "press SPACE to continue",
                self.window.width / 2,
                self.window.height / 2 - self.window.width / 25,
                arcade.csscolor.WHITE,
                24,
                anchor_x="center",
                anchor_y="center"
            )


    def on_show(self):
        """ Called when switching to this view
        """
        arcade.set_background_color(arcade.color.BLACK)
        # self.on_resize(self.window.width, self.window.height)

    def on_draw(self):
        """ Draw the intro screen
        """
        arcade.start_render()
        self._screen_msg.draw()
        if self._cont_msg:
            self._continue_msg.draw()

    def on_key_press(self, key, key_modfiers):
        """Called whenever a key on the keyboard is pressed.

        Args:
            key (int): key that was pressed.
            key_modifiers (int): key modifier that was pressed.
        """
        if key == arcade.key.SPACE:
            self.window.show_view(self.window.overworld)

# def resize(self, width, height):
#         if self._long_msg:
#             self._screen_msg = arcade.Text(
#                 self._message,
#                 width / 2,
#                 height / 2 + width / 12.5,
#                 arcade.csscolor.WHITE,
#                 36,
#                 anchor_x="center",
#                 anchor_y="center"
#             )
#         else:
#             self._screen_msg = arcade.Text(
#                 self._message,
#                 width / 2,
#                 height / 2 + width / 12.5,
#                 arcade.csscolor.WHITE,
#                 54,
#                 anchor_x="center",
#                 anchor_y="center"
#             )
#         if self._cont_msg:
#             self._continue_msg = arcade.Text(
#                 "press SPACE to continue",
#                 width / 2,
#                 height / 2 - width / 25,
#                 arcade.csscolor.WHITE,
#                 24,
#                 anchor_x="center",
#                 anchor_y="center"
#             )

