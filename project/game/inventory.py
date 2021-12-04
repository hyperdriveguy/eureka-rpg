import arcade

from game.ui_elements import Button, Selector

class Inventory(arcade.View):

    def __init__(self, inventory):
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
        pass

    def on_draw(self):
        arcade.start_render()
        self._scrolling_camera.use()
        self._selector.draw()

    def _scroll_camera(self):
        x, y = self._selector.selector_pos
        x -= self._scrolling_camera.viewport_width / 2
        y -= self._scrolling_camera.viewport_height / 2
        self._scrolling_camera.move_to((x, y))

    def on_update(self, delta_time):
        self._scroll_camera()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.W:
            self._selector.prev_button()
        if key == arcade.key.S:
            self._selector.next_button()
        if key == arcade.key.SPACE:
            pass

    def on_key_release(self, key, key_modifiers):
        pass

    def on_show_view(self):
        pass

    def on_resize(self, width: int, height: int):
        self._static_camera.resize(width, height)
        self._scrolling_camera.resize(width, height)
