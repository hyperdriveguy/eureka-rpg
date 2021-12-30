""" The game inventory """
import arcade
from game.ui_elements import Button, Selector

class Inventory(arcade.View):
    """ The inventory view

    Inherits: arcade.View

    Stereotype:

    Attributes:
        self._static_camera (arcade.Camera): an instance of arcade.Camera
        self._scrolling_camera (): an instance of arcade.Camera
        buttons (list): The list of buttons
        last_button_bottom (int): bottom of last button (center-y)
        self._selector (Selector): an instance of Selector
        self._selector.can_select (bool): Check if element can be selected
    """
    def __init__(self, inventory):
        """ Class Constructor

        Args:
            inventory (dict): Dictionary of the inventory
        """
        super().__init__()
        self._static_camera = arcade.Camera(self.window.width, self.window.height)
        self._scrolling_camera = arcade.Camera(self.window.width, self.window.height)
        buttons = []
        last_button_bottom = self._scrolling_camera.viewport_height / 2
        for possession, qty in inventory.items():
            buttons.append(Button(
                f'{possession} x{qty}',
                self._scrolling_camera.viewport_width / 2,
                last_button_bottom,
                arcade.color.BLACK,
                16,
                self._scrolling_camera.viewport_width,
                'center',
                anchor_x='center',
                anchor_y='top'
            ))
            last_button_bottom = buttons[-1][0].bottom - 2
        self._selector = Selector(buttons)
        self._selector.can_select = True

    def setup(self):
        """TODO"""

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()
        self._scrolling_camera.use()
        self._selector.draw()

    def _scroll_camera(self):
        """ move scroll camera. This selects different buttons
        """
        view_x, view_y = self._selector.selector_pos
        view_x -= self._scrolling_camera.viewport_width / 2
        view_y -= self._scrolling_camera.viewport_height / 2
        self._scrolling_camera.move_to((view_x, view_y))

    def on_update(self, delta_time):
        """ Scroll camera movement

        Args:
            delta_time (float, optional): time in seconds since method was last called.
        """
        self._scroll_camera()

    def on_key_press(self, key, key_modifiers):
        """Called whenever a key on the keyboard is pressed.

        Args:
            key (int): key that was pressed.
            key_modifiers (int): key modifier that was pressed.
        """
        if key == arcade.key.W:
            self._selector.prev_button()
        if key == arcade.key.S:
            self._selector.next_button()
        if key == arcade.key.SPACE:
            pass

    def on_key_release(self, key, key_modifiers):
        """Called whenever the user lets off a previously pressed key.

        Args:
            key (int): key that was pressed.
            key_modifiers (int): key modifier that was pressed.
        """

    def on_show_view(self):
        pass

    def on_resize(self, width: int, height: int):
        """ Called when screen is resized

        Args:
            width (int): width of camera
            height (int): height of camera
        """
        self._static_camera.resize(width, height)
        self._scrolling_camera.resize(width, height)
