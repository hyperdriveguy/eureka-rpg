import arcade

class Battle(arcade.View):

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)
    
    def setup(self):
        # Setup the Camera
        self.camera = arcade.Camera(self.window.width, self.window.height)

        # Setup the GUI Camera
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

    def on_draw(self):
        pass

    def on_update(self):
        pass

    def on_show_view(self):
        pass