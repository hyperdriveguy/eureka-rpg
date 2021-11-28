import arcade
from game.battle_player import BattlePlayer
from game.battle_hud import BattleHud
from game.contestant import Contestant

class Battle(arcade.View):

    def __init__(self):
        super().__init__()
        # Setup the Camera
        self._camera = arcade.Camera(self.window.width, self.window.height)

        # Setup the GUI Camera
        self._gui_camera = arcade.Camera(self.window.width, self.window.height)

        self._player = BattlePlayer()
        self._enemy = Contestant(['project/assets/player_placeholder.png', 'project/assets/player_placeholder_2.png', 'project/assets/player_placeholder_3.png'])
        self._player.center_x = self._camera.viewport_width / 5
        self._player.center_y = self._camera.viewport_height / 2
        self._enemy.center_x = self._camera.viewport_width * 4 / 5
        self._enemy.center_y = self._camera.viewport_height / 2
        self._contestants = arcade.SpriteList()
        self._contestants.append(self._player)
        self._contestants.append(self._enemy)

        self.battle_hud = BattleHud(self._gui_camera, self._player)
        
        arcade.set_background_color(arcade.color.WHITE)
    
    def setup(self):
        pass

    def on_draw(self):
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        self._gui_camera.use()
        self._contestants.draw()
        self.battle_hud.draw()

    def on_update(self, delta_time):
        self.battle_hud.update(delta_time)
        self._player.update_animation(delta_time)
        self._enemy.update_animation(delta_time)
    
    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.J:
            self._player.is_turn = not self._player.is_turn
        self.battle_hud.on_key_press(key, key_modifiers)

    def on_show_view(self):
        self._player.is_turn = True
    
    def on_resize(self, width: int, height: int):
        self._camera.resize(width, height)
        self._gui_camera.resize(width, height)
        self.battle_hud.resize_hud()
