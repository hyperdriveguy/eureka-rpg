""" Drawing the Text Box """
import textwrap
import arcade
from game import constants

class DrawTextBox:
    """ Responsible for drawing text boxes

    Attributes:
        self.rec_width (int): width of text box
        self.rec_length (int): length of text box
        self.text_box_center_x (int): horizontal position of the center point of the text box
        self.text_box_center_y (int): vertical position of the center point of the text box
        self.wrapper (TextWrapper): An instance of TextWrapper
        self.text_list (list): One string split into a list of strings to wrap the text
        self.num_lines (int): The number of lines the text list has (i.e the length of the text list)
        self.text (str): The text to be added to the text box
        self.cur_line (int): The last line added to the text box
        self.text_end (bool): Determine if the end of the text has been reached
        """
    def __init__(self, text, camera):
        """ Class Constructor
            Args:
                self (DrawTextBox): An instance of DrawTextBox
                text (str): The text to be printed in the text box
                camera (arcade.Camera): camera that will be drawn to
        """
        self._camera = camera
        self.rec_width = 500
        self.rec_length = 100
        self.resize(self._camera.viewport_width, self._camera.viewport_height)
        self.wrapper = textwrap.TextWrapper(width=45, drop_whitespace=False)
        self.text_list = self.wrapper.wrap(text)  # a list of strings
        self.num_lines = len(self.text_list)
        self.text = text
        self.cur_line = 0
        self.text_end = False
        self.create_page_text()

    def create_page_text(self):
        """ Create the text that will be seen in the text box.

            Args:
                self (DrawTextBox): Aself._character_face_direction[self._dir_priority]n instance of DrawTextBox
        """
        self.page_text = ''
        if self.num_lines >= 4:
            for index in range(self.cur_line, self.cur_line + 4):
                self.page_text += self.text_list[index]
            if self.cur_line + 4 == self.num_lines:
                self.text_end = True
        else:
            self.text_end = True

    def line_by_line(self):
        """ Go through text line by line and set current line.

            Args:
                self (DrawTextBox): An instance of DrawTextBox
        """
        self.cur_line += 1
        self.create_page_text()

    # def page_by_page(self):
    #     self.cur_line += 4
    #     self.create_page_text()

    def draw(self):
        """ Draw the text box background and text.

            Args:
                self (DrawTextBox): An instance of DrawTextBox
        """
        arcade.draw_rectangle_filled(self.text_box_center_x, self.text_box_center_y, self.rec_width, self.rec_length, arcade.csscolor.BLACK)
        arcade.draw_point(
            self.text_box_center_x,
            self.text_box_center_y,
            arcade.color.BARN_RED,
            5
            )
        if self.num_lines > 1:
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

    def resize(self, width: int, height: int):
        self.text_box_center_x = width / 2
        self.text_box_center_y = height - self.rec_length / 2 - 10
