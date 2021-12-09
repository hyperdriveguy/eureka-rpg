import arcade
from game.constants import GAME_NAME, SCREEN_WIDTH, SCREEN_HEIGHT
from game.ui_elements import Button, Selector

class IntroView(arcade.View):
    """ Splash screen for the game. Press spacebar to start game

    Inherits: arcade.View

    Stereotype: Controller

    Attributes:
        self._overworld (Overworld): an instance of Overworld
        self._text (arcade.Text): an instnace of acrade.Text. The text to display.
    """
    def __init__(self):
        """ Class Constructor
        """
        super().__init__()
        
        self._text = arcade.Text(
            GAME_NAME,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 35,
            arcade.csscolor.WHITE,
            48,
            anchor_x="center",
            anchor_y="center"
        )
        self._make_button()

    def _make_button(self):
        """Make the UI button for selecting an action.
        """
        # run_draw_x = round(self._gui_camera.viewport_width * 0.95)
        self._play_button = Button(
            'PLAY',
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 35,
            anchor_x='center',
            anchor_y='center',
            font_size=30,
            color=arcade.csscolor.WHITE
        )
        self._main_select = Selector([self._play_button],
                                                 y_mod=0.78, color=arcade.csscolor.WHITE)
        self._main_select.can_select = True

    def on_show(self):
        """ Called when switching to this view
        """
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Draw the intro screen
        """
        arcade.start_render()
        self._text.draw()
        self._main_select.draw()

    def on_key_press(self, key, key_modfiers):
        """Called whenever a key on the keyboard is pressed.

        Args:
            key (int): key that was pressed.
            key_modifiers (int): key modifier that was pressed.
        """
        if key == arcade.key.SPACE:
            self.window.show_view(self.window.overworld)
