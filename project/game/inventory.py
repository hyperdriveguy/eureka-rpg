import arcade

from game.ui_elements import Button, Selector

class Inventory(arcade.View):

    def __init__(self):
        super().__init__()
        self._static_camera = arcade.Camera(self.window.width, self.window.height)
        self._scrolling_camera = arcade.Camera(self.window.width, self.window.height)

    def setup(self):
        pass

    def on_draw(self):
        pass

    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, key_modifiers):
        pass

    def on_key_release(self, key, key_modifiers):
        pass

    def on_show_view(self):
        pass

    def on_resize(self, width: int, height: int):
        pass
