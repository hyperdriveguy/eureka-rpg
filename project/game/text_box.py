""" Drawing the Text Box """
import textwrap
import arcade
from game.utils import px_to_pt, pt_to_px, get_smallest

class DrawTextBox:
    """ Responsible for drawing text boxes

    Attributes:
        self._window (arcade.Window): an instance of arcade.Window
        self.page_text (str): the text for the page
        self.text (str): The text to be printed in the text box
        self.text_end (bool): check if the end of the text has been reached
        self.cur_line (int): The currrent line
        """
    def __init__(self, text: str, window: arcade.Window):
        """ Class Constructor
            Args:
                self (DrawTextBox): An instance of DrawTextBox
                text (str): The text to be printed in the text box
                camera (arcade.Camera): camera that will be drawn to
        """
        self._window = window
        self.page_text = ''
        self.text = text
        self.text_end = False
        self.resize(self._window.width, self._window.height)
        self.cur_line = 0

        self.create_page_text()

    def create_page_text(self):
        """ Create the text that will be seen in the text box.

            Args:
                self (DrawTextBox): An instance of DrawTextBox
        """
        self.page_text = ''
        if self.num_lines >= 3:
            for index in range(self.cur_line, self.cur_line + 3):
                try:
                    self.page_text += f'{self.text_list[index].strip()}\n'
                except IndexError:
                    pass
            if self.cur_line + 3 >= self.num_lines:
                self.text_end = True
        else:
            for line in self.text_list:
                self.page_text += line.strip(' ')
            self.text_end = True
        self._drawable_text.value = self.page_text

    def line_by_line(self):
        """ Go through text line by line and set current line.

            Args:
                self (DrawTextBox): An instance of DrawTextBox
        """
        self.cur_line += 1
        self.create_page_text()

    def page_by_page(self):
        """ Go through text page by page and set current line.

            Args:
                self (DrawTextBox): An instance of DrawTextBox
        """
        self.cur_line += 3
        self.create_page_text()

    def draw(self):
        """ Draw the text box background and text.

            Args:
                self (DrawTextBox): An instance of DrawTextBox
        """
        self._window_shape.draw()
        self._drawable_text.draw()

    def _calc_box_size(self, width, height):
        """Calculate textbox size from screen size.

        Args:
            width (int): screen width
            height (int): screen height
        """
        self._box_width = width * 0.625
        self._box_height = height * 0.15

    def _calc_font_size(self):
        """Calculate font size from box size.
        """
        based_on_height = px_to_pt(self._box_height / 8)
        based_on_width = px_to_pt(self._box_width / 33.5)
        self._font_size = get_smallest(based_on_height, based_on_width)

    def _wrap_text(self):
        """Preform text wrapping based on box size.

        This allows for better dynamic resizing.
        Newline chars are detected and manually broken in to lines.
        """
        text_bounds = self._box_width - (self._font_size * 4)
        char_width = int(text_bounds / pt_to_px(self._font_size))
        self.wrapper = textwrap.TextWrapper(width=char_width, drop_whitespace=False)
        broken_newlines = self.text.split('\n')
        self.text_list = []
        for line in broken_newlines:
            self.text_list.extend(self.wrapper.wrap(line))
        no_blank = lambda line: line.strip() != ''
        self.text_list = list(filter(no_blank, self.text_list))
        self.num_lines = len(self.text_list)

    def resize(self, width: int, height: int):
        """Resize and reposition the textbox.

        Args:
            width (int): new window width
            height (int): new window height
        """
        self.cur_line = -1
        self._calc_box_size(width, height)
        self._calc_font_size()
        self._wrap_text()
        self.text_box_center_x = width / 2
        self.text_box_center_y = height - self._box_height / 2 - height * 0.02
        if self.num_lines > 1:
            self._drawable_text = arcade.Text(
                self.page_text,
                self.text_box_center_x + pt_to_px(self._font_size) / 2,
                self.text_box_center_y - pt_to_px(self._font_size) / 2,
                arcade.csscolor.WHITE,
                self._font_size,
                font_name='mono',
                anchor_x="center",
                anchor_y="center",
                multiline=True,
                width=self._box_width
            )
        else:
            self._drawable_text = arcade.Text(
                self.page_text,
                self.text_box_center_x + pt_to_px(self._font_size) / 2,
                self.text_box_center_y - pt_to_px(self._font_size) / 2,
                arcade.csscolor.WHITE,
                self._font_size,
                anchor_x="center",
                anchor_y="center",
                width=self._box_width
            )
        self._window_shape = arcade.ShapeElementList()
        self._window_background = arcade.create_rectangle(
            self.text_box_center_x,
            self.text_box_center_y,
            self._box_width,
            self._box_height,
            arcade.csscolor.BLACK
        )
        self._window_border = arcade.create_rectangle(
            self.text_box_center_x,
            self.text_box_center_y,
            self._box_width,
            self._box_height,
            arcade.csscolor.WHITE,
            filled=False
        )
        self._window_shape.append(self._window_background)
        self._window_shape.append(self._window_border)
