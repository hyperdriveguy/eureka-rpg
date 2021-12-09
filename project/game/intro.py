import arcade

class IntroView(arcade.View):

    def __init__(self, window: arcade.Window = None):
        super().__init__(window=window)

    def on_draw(self):
        arcade.start_render()