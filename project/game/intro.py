import arcade
from game.constants import GAME_NAME, SCREEN_WIDTH, SCREEN_HEIGHT
from game.ui_elements import Button, Selector

class IntroView(arcade.View):

    def __init__(self):
        super().__init__()
        self._gui_camera = arcade.Camera(self.window.width, self.window.height)
        self._text = arcade.Text(
            GAME_NAME,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.csscolor.WHITE,
            24,
            anchor_x="center",
            anchor_y="center"
        )
        self._make_buttons()

        

    def _make_buttons(self):
        """Make the UI buttons for selecting an action.
        """
        # run_draw_x = round(self._gui_camera.viewport_width * 0.95)
        self._run_button = Button(
            'Play',
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 40,
            anchor_x='center',
            anchor_y='center',
            font_size=18,
            color=arcade.csscolor.WHITE
        )
        self._attack_button = Button(
            'Quit',
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 70,
            anchor_x='center',
            anchor_y='center',
            font_size=18,
            color=arcade.csscolor.WHITE
        )
        self._main_select = Selector((self._attack_button,
                                                 self._run_button),
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
        self._gui_camera.use()
        self._main_select.draw()


    def on_key_press(self, key, key_modfiers):
        """Called whenever a key on the keyboard is pressed.

        Args:
            key (int): key that was pressed.
            key_modifiers (int): key modifier that was pressed.
        """
        if key == arcade.key.W:
            self._main_select.prev_button()
        if key == arcade.key.S:
            self._main_select.next_button()
        
