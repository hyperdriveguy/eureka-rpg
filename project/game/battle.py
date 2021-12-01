"""Contains the battle engine.
"""
import sys
import arcade
from game.battle_player import BattlePlayer
from game.battle_hud import BattleHud
from game.contestant import Contestant
from game.utils import get_smallest


class Battle(arcade.View):
    """The battle view.

    This class directs all methods related to the battle engine.

    Inherits: arcade.View

    Stereotype: Controller
    """

    def __init__(self):
        """Basic battle initialization.

        These contain classes and values that should not have to be erased on battle restart.
        """
        super().__init__()
        # Setup the Camera
        self._camera = arcade.Camera(self.window.width, self.window.height)

        # Setup the GUI Camera
        self._gui_camera = arcade.Camera(self.window.width, self.window.height)

        self._player = BattlePlayer()
        self._enemy = Contestant(['project/assets/angry_cactus.png',
                                  'project/assets/angry_cactus_1.png',
                                  'project/assets/angry_cactus_2.png'])
        self._set_contestant_pos()
        self._contestants = arcade.SpriteList()
        self._contestants.append(self._player)
        self._contestants.append(self._enemy)
        self._timer = 0
        self._player_dmg = 0
        self._enemy_dmg = 0
        self._anim_done = True

        self.battle_hud = BattleHud(self._gui_camera, self._player)

        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):
        """Battle setup.

        This should be called when restarting the same battle.
        """
        pass

    def on_draw(self):
        """Draw elements on the screen.

        This command should happen before we start drawing. It will clear
        the screen to the background color, and erase what we drew last frame.
        """
        arcade.start_render()

        self._gui_camera.use()
        self.battle_hud.draw()

        self._camera.use()
        self._contestants.draw()
        if self._timer > 0:
            arcade.draw_text(f'-{self._player_dmg}',
                             self._player.center_x,
                             self._player.top,
                             color=arcade.color.RED)
            arcade.draw_text(f'-{self._enemy_dmg}',
                             self._enemy.center_x,
                             self._enemy.top,
                             color=arcade.color.RED)
            self._anim_done = False

    def _set_contestant_pos(self):
        """Set the position of the player and enemy on the screen.
        """
        self._player.center_x = self._camera.viewport_width / 5
        self._player.center_y = self._camera.viewport_height / 2
        self._enemy.center_x = self._camera.viewport_width * 4 / 5
        self._enemy.center_y = self._camera.viewport_height / 2
        self._player.scale = get_smallest(self._camera.viewport_width,
                                          self._camera.viewport_height) / 64 * 0.33
        self._enemy.scale = get_smallest(self._camera.viewport_width,
                                         self._camera.viewport_height) / 64 * 0.33

    def on_update(self, delta_time):
        """Preform updates for the battle view.

        Args:
            delta_time (float): time in seconds since method was last called.
        """
        self.battle_hud.update(delta_time)
        if self.battle_hud.has_selected:
            self._do_battle_turn()
        if self._timer <= 0 and self._player.is_turn is False:
            self.battle_hud.new_player_turn()
            self._player.is_turn = True
        if self._timer > 0:
            self._timer -= delta_time

        self._player.update_animation(delta_time)
        self._enemy.update_animation(delta_time)

    def _do_battle_turn(self):
        """Preform a battle turn based on player selection.

        Preforms several checks and calculates damage.
        """
        if self.battle_hud.player_action[0] == 'Attack':
            self._enemy_dmg = self.battle_hud.player_action[1]() - self._enemy.defend()
        self._player_dmg = self._enemy.attack() - self._player.defend()
        self._enemy.cur_hp -= self._enemy_dmg
        if self._enemy.cur_hp <= 0:
            self.window.show_view(self.window.overworld)
        self._player.cur_hp -= self._player_dmg
        if self._player.cur_hp <= 0:
            sys.exit()
        self._timer = 5
        self.battle_hud.update_hp()
        self.battle_hud.has_selected = False

    def on_key_press(self, key, key_modifiers):
        """Get player keypresses.

        Args:
            key (int): key that was pressed.
            key_modifiers (int): key modifier that was pressed.
        """
        if key == arcade.key.J:
            self._player.is_turn = not self._player.is_turn
        self.battle_hud.on_key_press(key, key_modifiers)

    def on_show_view(self):
        """Called when the window shows the view.
        """
        self._player.is_turn = True

    def on_resize(self, width: int, height: int):
        """Called whenever the user resizes the window.

        Args:
            width (int): new window width.
            height (int): new window height.
        """
        self._camera.resize(width, height)
        self._gui_camera.resize(width, height)
        self.battle_hud.resize_hud()
        self._set_contestant_pos()
