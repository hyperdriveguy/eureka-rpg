import arcade
import textwrap

class DrawTextBox:

    def __init__(self, text):
        self.rec_width = 300    
        self.rec_length = 200
        self.text = text
    
    def draw_text_box(self, center_x, center_y):
        arcade.draw_rectangle_filled(center_x, center_y, self.rec_width, self.rec_length, arcade.csscolor.BLACK)
        wrapper = textwrap.TextWrapper(width=35)
        self.text = wrapper.wrap(self.text) #a list of strings
        text_x = center_x - self.rec_width / 2 + 10
        text_y = center_y + self.rec_length / 2 - 10
        for line in self.text:
            text_y -= 25
            arcade.draw_text(
                line,
                text_x,
                text_y,
                arcade.csscolor.WHITE,
                14,
            )