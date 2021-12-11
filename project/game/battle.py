"""Contains the battle engine.
"""
import arcade

from game.battle_hud import BattleHud
from game.battle_player import BattlePlayer
from game.enemy_switcher import EnemySwitcher
from game.text_box import DrawTextBox
from game.timer import Timer
from game.utils import get_smallest, article_selector


class Battle(arcade.View):
    """The battle view.

    This class directs all methods related to the battle engine.

    Inherits: arcade.View

    Stereotype: Controller

    Attributes:
        self._camera (arcade.Camera): an instance of arcade.Camera
        self._gui_camera (arcade.Camera): ui camera - an instance of arcade.Camera

        self._player (BattlePlayer): an instance of BattlePlayer
        self._enemy = (Contestant): an instance of Contestant
        self._contestants (arcade.SpriteList): list of contestants as sprites

        self._timer (Timer): a timer
        self._player_dmg (int): player damage
        self._enemy_dmg (int): enemy damage
        self._anim_done (bool): is animation done
        self.battle_hud (BattleHud): an instance of BattleHud
    """
    def __init__(self, enemy_name):
        """Basic battle initialization.

        These contain classes and values that should not have to be erased on battle restart.
        """
        super().__init__()
        # Init Enemies
        self._enemy_switcher = EnemySwitcher()

        # Setup the Camera
        self._camera = arcade.Camera(self.window.width, self.window.height)

        # Setup the GUI Camera
        self._gui_camera = arcade.Camera(self.window.width, self.window.height)

        self._battle_textbox = DrawTextBox(f'{article_selector(enemy_name).title()} {enemy_name.title()} approaches!', self.window)
        self._active_textbox = True

        self._player = BattlePlayer()
        self._enemy = self._enemy_switcher.get_enemy(enemy_name)
        self._set_contestant_pos()
        self._contestants = arcade.SpriteList()
        self._contestants.append(self._player)
        self._contestants.append(self._enemy)

        self._player_turn_timer = Timer(2)
        self._enemy_turn_timer = Timer(2)

        self._player_first = False
        self._turns_in_progress = False

        self._player_dmg = 0
        self._enemy_dmg = 0
        self._anim_done = True

        self.battle_hud = BattleHud(self._gui_camera, self._player)

        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):
        """Battle setup.

        This should be called when restarting the same battle.
        """

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
        if self._enemy_turn_timer.active:
            arcade.draw_text(f'-{self._player_dmg}',
                             self._player.center_x,
                             self._player.top,
                             color=arcade.color.RED)
        if self._player_turn_timer.active:
            arcade.draw_text(f'-{self._enemy_dmg}',
                             self._enemy.center_x,
                             self._enemy.top,
                             color=arcade.color.RED)

        if self._active_textbox:
            self._battle_textbox.draw()

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
        self._player.update_animation(delta_time)
        self._enemy.update_animation(delta_time)

        if self._active_textbox:
            return

        if self.battle_hud.has_selected and not self._turns_in_progress:
            self._player.is_turn = False
            self._turns_in_progress = True
            self._turn_order()
        if self._player_turn_timer.done:
            self._player_turn_timer.pause()
            self._dead_enemy_check()
            if self.battle_hud.player_action == 'Run':
                # attempt to run away
                run_chance = self._player.speed_check() - self._enemy.speed_check()
                if run_chance > 1:
                    self.window.show_view(self.window.overworld)
            if self._player_first:
                self._enemy_turn()
                self._enemy_turn_timer.restart()
            else:
                self._new_player_choice()
        if self._enemy_turn_timer.done:
            self._enemy_turn_timer.pause()
            self._dead_player_check()
            if not self._player_first:
                self._player_turn()
                self._player_turn_timer.restart()
            else:
                self._new_player_choice()


        self._player_turn_timer.update(delta_time)
        self._enemy_turn_timer.update(delta_time)


    def _new_player_choice(self):
        self._turns_in_progress = False
        self.battle_hud.has_selected = False
        self._turns_in_progress = False
        self.battle_hud.new_player_turn()
        self._player.is_turn = True

    def _turn_order(self):
        if self._player.speed_check() > self._enemy.speed_check():
            self._player_first = True
            self._player_turn()
            self._player_turn_timer.restart()
        else:
            self._player_first = False
            self._enemy_turn()
            self._enemy_turn_timer.restart()

    def _player_turn(self):
        if self.battle_hud.player_action == 'Attack':
            self._enemy_dmg = max((self._player.attack() - self._enemy.defend(), 0))
            self._enemy.cur_hp -= self._enemy_dmg

    def _enemy_turn(self):
        self._player_dmg = max((self._enemy.attack() - self._player.defend(), 0))
        self._player.cur_hp -= self._player_dmg
        self.battle_hud.update_hp()

    def _dead_enemy_check(self):
        if self._enemy.cur_hp <= 0:
            self.window.show_view(self.window._win_battle)

    def _dead_player_check(self):
        if self._player.cur_hp <= 0:
            self.window.show_view(self.window.death_screen)

    def on_key_press(self, key, key_modifiers):
        """Get player keypresses.

        Args:
            key (int): key that was pressed.
            key_modifiers (int): key modifier that was pressed.
        """
        if self._active_textbox and key == arcade.key.SPACE:
            #arcade.play_sound(self.jump_sound)
            if self._battle_textbox.text_end:
                self._active_textbox = False
            else:
                self._battle_textbox.line_by_line()
            return
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
