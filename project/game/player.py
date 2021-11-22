import arcade
from game import constants
from game.utils import is_between

class Player(arcade.Sprite):
    """Contains functions of the player.

    This class is primarily overworld oriented.
    Stereotype: Information Holder.

    Inherits the Sprite class.
    """

    def __init__(self):
        super().__init__()

        # Default to face-down
        self._character_face_direction = [constants.Direction.FACE_NONE ,constants.Direction.FACE_DOWN]

        # Used for flipping between image sequences
        self._cur_texture = 0
        self._force_walk_texture = False
        self._force_walk_update_counter = 0

        self._scale = constants.CHARACTER_SCALING

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

    def _can_interact(self, shape, map_height):
        begin_x = round(shape[0][0] * constants.TILE_SCALING)
        end_x = round(shape[1][0] * constants.TILE_SCALING)
        end_y = round(shape[0][1] * constants.TILE_SCALING) + map_height
        begin_y = round(shape[2][1] * constants.TILE_SCALING) + map_height
        if self.character_face_y == constants.Direction.FACE_UP.name:
            begin_y -= 10
            coll_side_y = self.top
        elif self.character_face_y == constants.Direction.FACE_DOWN.name:
            end_y += 10
            coll_side_y = self.bottom
        else:
            coll_side_y = self.center_y

        if self.character_face_x == constants.Direction.FACE_LEFT.name:
            end_x += 10
            coll_side_x = self.left
        elif self.character_face_x ==  constants.Direction.FACE_RIGHT.name:
            begin_x -= 10
            coll_side_x = self.right
        else:
            coll_side_x = self.center_x

        if (is_between(coll_side_x, begin_x, end_x) and
                is_between(coll_side_y, begin_y, end_y)):
            return True
        return False
    


    @property
    def character_face_direction(self):
        return f'{self._character_face_direction[0].name[5:]}, {self._character_face_direction[1].name[5:]}'
    
    @property
    def character_face_x(self):
        return self._character_face_direction[0].name
    
    @property
    def character_face_y(self):
        return self._character_face_direction[1].name

    @character_face_x.setter
    def character_face_x(self, character_face_x):
        if isinstance(character_face_x, constants.Direction):
            self._character_face_direction[0] = character_face_x
            self._force_walk_texture = True

    @character_face_y.setter
    def character_face_y(self, character_face_y):
        if isinstance(character_face_y, constants.Direction):
            self._character_face_direction[1] = character_face_y
            self._force_walk_texture = True

