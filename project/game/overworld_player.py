import arcade
from game import constants
from game.utils import is_between

class OverworldPlayer(arcade.Sprite):
    """Contains functions of the player.

    This class is primarily overworld oriented.
    Stereotype: Information Holder.

    Inherits the Sprite class.
    """

    def __init__(self):
        super().__init__()

        # Default to face-down
        self._character_face_direction = [constants.FACE_NONE , constants.FACE_DOWN]

        # Used for flipping between image sequences
        self._cur_texture = 0
        self._force_walk_texture = False
        self._force_walk_update_counter = 0

        self._scale = constants.CHARACTER_SCALING

        self._movement_lock = False

        self._left_pressed = False
        self._right_pressed = False
        self._up_pressed = False
        self._down_pressed = False

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        #self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # --- Load Textures ---

        # Images from Kenney.nl's Asset Pack 3
        #main_path = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"
        # main_path = ":resources:images/animated_characters/female_person/femalePerson"
        # main_path = ":resources:images/animated_characters/male_person/malePerson"
        # main_path = ":resources:images/animated_characters/male_adventurer/maleAdventurer"
        # main_path = ":resources:images/animated_characters/zombie/zombie"
        # main_path = ":resources:images/animated_characters/robot/robot"

        # Load textures for idle standing
        #self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self._idle_texture = arcade.load_texture('project/assets/placeholder.png')
        self.texture = self._idle_texture

        # Load textures for walking
        self._walk_textures = []
        self._walk_textures.append(arcade.load_texture('project/assets/placeholder_step.png'))
        self._walk_textures.append(arcade.load_texture('project/assets/placeholder.png'))
        self._walk_textures.append(arcade.load_texture('project/assets/placeholder.png', flipped_horizontally=True))
        self._walk_textures.append(arcade.load_texture('project/assets/placeholder_step.png', flipped_horizontally=True))
        #for i in range(8):
        #    texture = load_texture_pair(f"{main_path}_walk{i}.png")
        #    self.walk_textures.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        #if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
        #    self.character_face_direction = LEFT_FACING
        #elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
        #    self.character_face_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0 and not self._force_walk_texture:
            self.texture = self._idle_texture
            return

        # Walking animation
        self._cur_texture += 1
        if self._cur_texture >= len(self._walk_textures) * constants.UPDATES_PER_FRAME:
            self._cur_texture = 0
        frame = self._cur_texture // constants.UPDATES_PER_FRAME
        #direction = self.character_face_direction
        self.texture = self._walk_textures[frame]#[direction]
        if self._force_walk_texture and self._force_walk_update_counter < 1/30:
            self._force_walk_update_counter += delta_time
        else:
            self._force_walk_texture = False
            self._force_walk_update_counter = 0

    def on_update(self, delta_time: float = 1 / 60):
        if self._movement_lock:
            return
        if self._up_pressed and not self._down_pressed:
            if self.character_face_y == constants.FACE_UP:
                self.change_y = constants.PLAYER_MOVEMENT_SPEED
            self.character_face_y = constants.FACE_UP
        elif self._down_pressed and not self._up_pressed:
            if self.character_face_y == constants.FACE_DOWN:
                self.change_y = -constants.PLAYER_MOVEMENT_SPEED
            self.character_face_y = constants.FACE_DOWN
        else:
            self.change_y = 0
            if self.character_face_x != constants.FACE_NONE and self.change_x != 0:
                self.character_face_y = constants.FACE_NONE


        if self._left_pressed and not self._right_pressed:
            if self.character_face_x == constants.FACE_LEFT:
                self.change_x = -constants.PLAYER_MOVEMENT_SPEED
            self.character_face_x = constants.FACE_LEFT
        elif self._right_pressed and not self._left_pressed:
            if self.character_face_x == constants.FACE_RIGHT:
                self.change_x = constants.PLAYER_MOVEMENT_SPEED
            self.character_face_x = constants.FACE_RIGHT
        else:
            self.change_x = 0
            if self.character_face_y != constants.FACE_NONE and self.change_y != 0:
                self.character_face_x = constants.FACE_NONE

    def on_key_press(self, key, key_modifiers):
        self._flag_key_movement(key, True)
    
    def on_key_release(self, key, key_modifiers):
        self._flag_key_movement(key, False)

    def _flag_key_movement(self, key, is_pressed):
        if key in (arcade.key.UP, arcade.key.W):
            self._up_pressed = is_pressed
        if key in (arcade.key.DOWN, arcade.key.S):
            self._down_pressed = is_pressed
        if key in (arcade.key.LEFT, arcade.key.A):
            self._left_pressed = is_pressed
        if key in (arcade.key.RIGHT, arcade.key.D):
            self._right_pressed = is_pressed

    def force_movement_stop(self):
        self.change_x = 0
        self.change_y = 0
        self._movement_lock = True

    @property
    def allow_player_input(self):
        return self._movement_lock
    
    @allow_player_input.setter
    def allow_player_input(self, allow_player_input: bool):
        self._movement_lock = not allow_player_input
    
    @property
    def character_face_x(self):
        return self._character_face_direction[0]
    
    @property
    def character_face_y(self):
        return self._character_face_direction[1]

    @character_face_x.setter
    def character_face_x(self, character_face_x):
        if character_face_x in (constants.FACE_LEFT, constants.FACE_RIGHT, constants.FACE_NONE):
            self._character_face_direction[0] = character_face_x
            self._force_walk_texture = True

    @character_face_y.setter
    def character_face_y(self, character_face_y):
        if character_face_y in (constants.FACE_DOWN, constants.FACE_UP, constants.FACE_NONE):
            self._character_face_direction[1] = character_face_y
            self._force_walk_texture = True

    @property
    def character_face_direction(self):
        return f'{self._character_face_direction[0]}, {self._character_face_direction[1]}'

    @property
    def player_highlighted(self):
        return (self.color == arcade.color.RED)
    
    @player_highlighted.setter
    def player_highlighted(self, player_highlighted):
        self.color = arcade.color.RED if player_highlighted else arcade.color.WHITE
