import arcade
import textwrap
from game import constants

class DrawTextBox:

    def __init__(self, text):
        self.rec_width = 500    
        self.rec_length = 100
        self.text_box_center_x = constants.SCREEN_WIDTH / 2
        self.text_box_center_y = constants.SCREEN_HEIGHT - self.rec_length / 2 - 10
        self.wrapper = textwrap.TextWrapper(width=55)
        self.text_list = self.wrapper.wrap(text) #a list of strings
        self.text = text
    

    def draw_text_box(self):
        arcade.draw_rectangle_filled(self.text_box_center_x, self.text_box_center_y, self.rec_width, self.rec_length, arcade.csscolor.BLACK)
        arcade.draw_point(self.text_box_center_x, self.text_box_center_y, arcade.color.BARN_RED, 5)
        if len(self.text_list) > 1:
            arcade.draw_text(
                self.text,
                self.text_box_center_x,
                self.text_box_center_y,
                arcade.csscolor.WHITE,
                14,
                anchor_x="center",
                anchor_y="center",
                multiline=True,
                width=self.rec_width - 15
            )                
        else:
            arcade.draw_text(
                self.text,
                self.text_box_center_x,
                self.text_box_center_y,
                arcade.csscolor.WHITE,
                14,
                anchor_x="center",
                anchor_y="center",
            )
