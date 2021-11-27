import arcade
import textwrap
from game import constants

class DrawTextBox:

    def __init__(self, text):
        self.rec_width = 500    
        self.rec_length = 100
        self.text_box_center_x = constants.SCREEN_WIDTH / 2
        self.text_box_center_y = constants.SCREEN_HEIGHT - self.rec_length / 2 - 10
        self.wrapper = textwrap.TextWrapper(width=45)
        self.text_list = self.wrapper.wrap(text) #a list of strings
        self.text = text
        self.cur_line = 0
        self.text_end = False
        self.create_page_text()

    def create_page_text(self):
        self.page_text = ''
        for index in range(self.cur_line, self.cur_line + 4):
            self.page_text += self.text_list[index] 
        # print(self.text_list)
        if self.cur_line + 4 == len(self.text_list):
            self.text_end = True 


    def line_by_line(self):
        self.cur_line += 1
        self.create_page_text()
    
    def page_by_page(self):
        self.cur_line += 4
        self.create_page_text()

    def draw_text_box(self):
        arcade.draw_rectangle_filled(self.text_box_center_x, self.text_box_center_y, self.rec_width, self.rec_length, arcade.csscolor.BLACK)
        arcade.draw_point(self.text_box_center_x, self.text_box_center_y, arcade.color.BARN_RED, 5)
        if len(self.text_list) > 1:
            arcade.draw_text(
                self.page_text,
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
