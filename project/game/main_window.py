import arcade
import random
from game import constants
from pyglet.math import Vec2

class MainWindow(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        self.free_camera = False
        self.free_coords = 0, 0
        
        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        # Keep track of the score
        self.score = 0
        self.show_score = True

        # Where is the right edge of the map?
        self.end_of_map = 0

        # Level
        self.level = 1

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")

        arcade.set_background_color(arcade.color.DENIM)

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """

        # Setup the Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Setup the GUI Camera
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Name of map file to load
        map_name = "project/assets/test_map.json"
        #map_name = f":resources:tiled_maps/map2_level_{self.level}.json"


        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
            "Coins": {
                "use_spatial_hash": True,
            },
            "Don't Touch": {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, constants.TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        print(self.scene['Platforms'])

        # Keep track of the score
        self.score = 0

        # Create the Sprite lists
        self.scene.add_sprite_list("Player")

        # Add Player Spritelist before "Foreground" layer. This will make the foreground
        # be drawn after the player, making it appear to be in front of the Player.
        # Setting before using scene.add_sprite allows us to define where the SpriteList
        # will be in the draw order. If we just use add_sprite, it will be appended to the
        # end of the order.
        self.scene.add_sprite_list_before("Player", 'Foreground')

        # Set up the player, specifically placing it at these coordinates.
        # image_source = ":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png"
        image_source = 'project/assets/placeholder.png'
        self.player_sprite = arcade.Sprite(image_source, constants.CHARACTER_SCALING)
        self.player_sprite.center_x = constants.PLAYER_START_X
        self.player_sprite.center_y = constants.PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=0, walls=self.scene['Platforms']
        )

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = self.tile_map.width * 64 #GRID_PIXEL_SIZE

        self.yeet_layer = self.tile_map.object_lists["Object Layer 1"]

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below

        # Activate our Camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()

        if self.show_score:
            # Activate the GUI camera before drawing GUI elements
            self.gui_camera.use()

            # Draw our score on the screen, scrolling it with the viewport
            score_text = f"Score: {self.score}"
            arcade.draw_text(
                score_text,
                10,
                10,
                arcade.csscolor.WHITE,
                18,
            )

        for box in self.yeet_layer:
            print(box.properties, '\n\n\n\n\n')
            try:
                text = box.properties["text"]
                print(box.shape)
                print(range(box.shape[0][0], box.shape[1][0]))
                print(range(-box.shape[0][1], -box.shape[2][1]))
                if self.player_sprite.center_x in range(box.shape[0][0] * constants.TILE_SCALING, box.shape[1][0] * constants.TILE_SCALING) and self.player_sprite.center_y in range(-box.shape[0][1] * constants.TILE_SCALING, -box.shape[2][1] * constants.TILE_SCALING):
                    arcade.draw_text(
                        text,
                        constants.SCREEN_WIDTH - 200,
                        10,
                        arcade.csscolor.WHITE,
                        18,
                    )
                    print('in da box')
                print(self.player_sprite.center_x, self.player_sprite.center_y)
            except KeyError:
                print('Warning: Interactable has no assigned text.')

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = [screen_center_x, screen_center_y]
        self.free_coords = player_centered

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """

        # Move the player with the physics engine
        self.physics_engine.update()

        # Position the camera
        if not self.free_camera:
            self.center_camera_to_player()

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Add one to the score
            self.score += 1

        # See if the user got to the end of the level
        if self.player_sprite.center_x >= self.end_of_map:
            # Advance to the next level
            self.level += 1

            # Load the next level
            self.setup()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = constants.PLAYER_MOVEMENT_SPEED

        if key == arcade.key.SPACE:
            arcade.play_sound(self.jump_sound)
        
        if key == arcade.key.F11:
            if not self.fullscreen:
                self.set_fullscreen(True)
                self.setup()
            else:
                self.set_fullscreen(False)
                self.setup()

        if key == arcade.key.RCTRL:
            if self.show_score:
                self.show_score = False
            else:
                self.show_score = True

        if key == arcade.key.Z:
            if self.free_camera:
                self.free_camera = False
            else:
                self.free_camera = True

        if self.free_camera:
            if key == arcade.key.T:
                self.camera.shake(Vec2(10,10))
            
            if key == arcade.key.L:
                self.free_coords[0] += 64
                self.camera.move_to(self.free_coords)

            if key == arcade.key.K:
                self.free_coords[1] -= 64
                self.camera.move_to(self.free_coords)
                
            if key == arcade.key.J:
                self.free_coords[0] -= 64
                self.camera.move_to(self.free_coords)
                
            if key == arcade.key.I:
                self.free_coords[1] += 64
                self.camera.move_to(self.free_coords)

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

