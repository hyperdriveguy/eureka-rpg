import arcade
from game.battle_player import BattlePlayer
from game import ui_elements
from game.utils import px_to_pt, pt_to_px, get_smallest

class BattleHud:
    
    def __init__(self, gui_camera: arcade.Camera, player: BattlePlayer):
        self._gui_camera = gui_camera
        self._player = player
        self._has_selected = False
        self.new_player_turn()

        # Build shapes/sprites
        self._hud_shape = arcade.ShapeElementList()
        self._hp_sprite_list = arcade.SpriteList()
        self._font_size = self._calc_base_font_size()
        self._create_hp_indicator()
        self._make_buttons()
        self._hp_sprite_list.append(self._cur_hp_sprite)
        self._hp_sprite_list.append(self._full_hp_sprite)
        self._build_shapes()
        self._build_tab()

    def _create_hp_indicator(self):
        hp_draw_x = round(self._gui_camera.viewport_width * 0.05)
        cur_hp_draw_y = round(self._gui_camera.viewport_height * 0.18)
        self._cur_hp_sprite = arcade.create_text_sprite(
            str(self._player._cur_heart_points),
            hp_draw_x,
            cur_hp_draw_y,
            align='center',
            anchor_x='left',
            anchor_y='center',
            font_size=self._font_size,
            color=arcade.color.LIGHT_GREEN)
        base_hp_draw_y = self._cur_hp_sprite.bottom
        self._full_hp_sprite = arcade.create_text_sprite(
            f'/ {self._player._base_heart_points}',
            hp_draw_x,
            base_hp_draw_y,
            anchor_x='left',
            anchor_y='top',
            font_size=self._font_size * 0.7,
            color=arcade.color.WHITE
        )

    def _make_buttons(self,):
        run_draw_x = round(self._gui_camera.viewport_width * 0.95)
        self._run_button = ui_elements.Button(
            'Run',
            run_draw_x,
            self._gui_camera.viewport_height * 0.005,
            anchor_x='right',
            anchor_y='bottom',
            font_size=self._font_size * 0.7,
            color=arcade.color.WHITE
        )
        self._attack_button = ui_elements.Button(
            'Attack',
            self._run_button[0].left - self._gui_camera.viewport_width * 0.05,
            self._gui_camera.viewport_height * 0.005,
            anchor_x='right',
            anchor_y='bottom',
            font_size=self._font_size * 0.7,
            color=arcade.color.WHITE
        )
        self._main_select = ui_elements.Selector(self._attack_button, self._run_button)

    def _calc_base_font_size(self):
        hp_font_size_h = round(px_to_pt(self._gui_camera.viewport_height * 0.08))
        hp_font_size_w = round(px_to_pt(self._gui_camera.viewport_width / 12 * 0.8))
        return get_smallest(hp_font_size_h, hp_font_size_w)
        
    def _build_shapes(self):
        # Build main bar
        main_bar_height = round(self._gui_camera.viewport_height * 0.1)
        main_bar_height = max(main_bar_height, 20)
        main_bar_center_y = round(main_bar_height / 2)
        main_bar_center_x = round(self._gui_camera.viewport_width /  2)
        main_bar = arcade.create_rectangle(main_bar_center_x, main_bar_center_y, self._gui_camera.viewport_width, main_bar_height, arcade.color.BRONZE)
        two_tone_bar = arcade.create_rectangle(main_bar_center_x, main_bar_center_y, self._gui_camera.viewport_width, self._run_button[0].height, arcade.color.BRONZE_YELLOW)
        self._hud_shape.append(two_tone_bar)
        self._hud_shape.append(main_bar)
    
    def _build_tab(self):
        # Build circular tab
        center_x = self._cur_hp_sprite.center_x
        center_y = self._cur_hp_sprite.bottom
        tab_width = self._cur_hp_sprite.width * 1.4 #self._gui_camera.viewport_width / 6
        tab_height = self._cur_hp_sprite.top * 1.3
        self._tab = arcade.create_ellipse(
            center_x,
            center_y,
            tab_width,
            tab_height,
            arcade.color.BRONZE)
        self._hud_shape.append(self._tab)

    def resize_hud(self):
        self._font_size = self._calc_base_font_size()
        # Clear list and rebuild
        self._hud_shape = arcade.ShapeElementList()
        self.update_hp()
        self._build_shapes()
    
    def _get_action(self, action):
        if action == 'Attack':
            self._selected_action = (action, self._player.attack)
        elif action == 'Run':
            self._selected_action = (action, None)
        else:
            raise ValueError(f'Unhandled action "{action}"')
    
    def update_hp(self):
        self._hp_sprite_list.remove(self._cur_hp_sprite)
        self._hp_sprite_list.remove(self._full_hp_sprite)
        self._create_hp_indicator()
        self._hp_sprite_list.append(self._cur_hp_sprite)
        self._hp_sprite_list.append(self._full_hp_sprite)
        try:
            self._hud_shape.remove(self._tab)
        except ValueError:
            pass
        self._build_tab()
        
    
    def update(self, delta_time):
        self._main_select.can_select = (self._player.is_turn and not self._has_selected)
        
    
    def draw(self):
        self._hud_shape.draw()
        self._hp_sprite_list.draw()
        self._main_select.draw()
    
    def on_key_press(self, key, key_modifiers):
        if self._player.is_turn:
            if key == arcade.key.A:
                self._main_select.prev_button()
            if key == arcade.key.D:
                self._main_select.next_button()
            if key == arcade.key.SPACE:
                self._get_action(self._main_select.select())
                self._player.is_turn = False
                self._has_selected = True

    def new_player_turn(self):
        self._selected_action = ('', None)
    
    @property
    def player_action(self):
        return self._selected_action
    
    @property
    def has_selected(self):
        return self._has_selected

    @has_selected.setter
    def has_selected(self, has_selected):
        self._has_selected = has_selected
