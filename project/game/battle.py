import arcade
from game.battle_player import BattlePlayer
from game.battle_hud import BattleHud

class Battle(arcade.View):

    def __init__(self):
        super().__init__()
        # Setup the Camera
        self._camera = arcade.Camera(self.window.width, self.window.height)

        # Setup the GUI Camera
        self._gui_camera = arcade.Camera(self.window.width, self.window.height)

        self._player = BattlePlayer()

        self.battle_hud = BattleHud(self._gui_camera, self._player)
        
        arcade.set_background_color(arcade.color.WHITE)
    
    def setup(self):
        pass

    def on_draw(self):
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        self._gui_camera.use()
        self.battle_hud._hud_shape.draw()
        self.battle_hud._hp_sprite_list.draw()

    def on_update(self, delta_time):
        pass

    def on_show_view(self):
        pass
    
    def on_resize(self, width: int, height: int):
        self._camera.resize(width, height)
        self._gui_camera.resize(width, height)
        self.battle_hud.resize_hud()
