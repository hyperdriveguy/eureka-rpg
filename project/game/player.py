import arcade
from game import constants

class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()

        # Default to face-right
        #self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self._cur_texture = 0

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
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self._idle_texture
            return

        # Walking animation
        self._cur_texture += 1
        if self._cur_texture >= len(self._walk_textures) * constants.UPDATES_PER_FRAME:
            self._cur_texture = 0
        frame = self._cur_texture // constants.UPDATES_PER_FRAME
        #direction = self.character_face_direction
        self.texture = self._walk_textures[frame]#[direction]

