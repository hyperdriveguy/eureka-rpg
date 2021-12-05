"""Contains reusable UI elements.
"""
from typing import Iterable
import arcade


class Button(arcade.SpriteList):
    """A selectable button with a text indicator.

    Inherits: arcade.Spritelist

    Stereotype: Information Holder

    Attributes:
        self._action_name (str): The name of the action the player can take

        self._button_text (text sprite): The text of the button as a sprite
    """
    def __init__(self,
                 text: str,
                 start_x: float,
                 start_y: float,
                 color: arcade.Color,
                 font_size: float = 12,
                 width: int = 0,
                 align: str = "left",
                 font_name=("calibri", "arial"),
                 anchor_x: str = "left",
                 anchor_y: str = "baseline",
                 rotation: float = 0,
                 ):
        """Initialize the button sprite and attributes.

        Args:
            text (str): text to display on button.
            start_x (float): start x position in pixels.
            start_y (float): start y position in pixels.
            color (arcade.Color): text color.
            font_size (float, optional): Font size in points.
                Defaults to 12.
            width (int, optional): max text width.
                Defaults to 0.
            align (str, optional): text alignment.
                Defaults to "left".
            font_name (tuple, optional): font name to use.
                Defaults to ("calibri", "arial").
            anchor_x (str, optional): place to anchor start_x.
                Defaults to "left".
            anchor_y (str, optional): place to anchor start_y.
                Defaults to "baseline".
            rotation (float, optional): degrees that text should be rotated.
                Defaults to 0.
        """
        super().__init__()

        self._action_name = text

        self._button_text = arcade.create_text_sprite(
            text,
            start_x,
            start_y,
            color,
            font_size=font_size,
            width=width,
            align=align,
            font_name=font_name,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            rotation=rotation
            )
        self.append(self._button_text)

    def clear(self):
        """
        Raises:
            NotImplementedError: message if error: UI elements are not clearable
        """
        raise NotImplementedError('UI elements are not clearable.')

    @property
    def name(self):
        """Text shown on the button.

        Returns:
            str: name of the button.
        """
        return self._action_name


class Selector:
    """Contains selectable UI elements and determines if they are highlighted.

    Stereotype: Controller

    Attributes:
        self._y_mod (int): y point modification
        self._button_actions (dict): Dictionary of the button actions
        self._button_list (arcade.SpriteList): an instance of arcade.SpriteList()
        self._cur_selection (int): The element that is selected

        self._selector_list (arcade.ShapeElementList): an instance of arcade.ShapeElementList()
        self._can_select (bool): Check if element can be selected
    """

    def __init__(self, buttons: Iterable, orient='main', y_mod=1):
        """Initialize the selector with the containing UI elements.

        Args:
            orient (str, optional): determine whether navigation is 1-D or 2-D.
                Defaults to 'main'. Not yet implemented.
            y_mod (int): default 1.
        Raises:
            IndexError: an empty sprite list was provided.
        """
        self._y_mod = y_mod
        self._button_actions = {}
        self._button_list = arcade.SpriteList()
        for button in buttons:
            if len(button) > 1:
                raise IndexError('Invalid button was passed to the selector.')
            self._button_list.extend(button)
            self._button_actions[button[0]] = button.name
        self._cur_selection = 0
        # print('button list',len(self._button_list))
        # print('buttons', len(buttons))

        self._selector_list = arcade.ShapeElementList()
        self._add_selector()
        self._can_select = False

    def _add_selector(self):
        """Create and append the selector element to the list.
        """
        self._selection_box = arcade.create_rectangle(
            self._button_list[self._cur_selection].center_x,
            self._button_list[self._cur_selection].center_y * self._y_mod,
            self._button_list[self._cur_selection].width * 1.1,
            self._button_list[self._cur_selection].height * 0.8,
            arcade.color.BLACK,
            border_width=3,
            filled=False
        )
        self._selector_list.append(self._selection_box)

    def next_button(self):
        """Select the next button in the selector list.
        """
        self._cur_selection += 1
        if self._cur_selection >= len(self._button_list):
            self._cur_selection = 0
        self._update_selector()

    def prev_button(self):
        """Select the previous button in the selector list.
        """
        self._cur_selection -= 1
        if self._cur_selection < 0:
            self._cur_selection = len(self._button_list) - 1
        self._update_selector()

    def select(self):
        """Select the current button.

        Returns:
            str: name of the selected button.
        """
        return self._button_actions[self._button_list[self._cur_selection]]

    def _update_selector(self):
        """Update the selector sprite by recreating it.
        """
        self._selector_list.remove(self._selection_box)
        self._add_selector()

    def draw(self):
        """Draw all the buttons and the selector if able to select.
        """
        self._button_list.draw()
        if self._can_select:
            self._selector_list.draw()

    @property
    def can_select(self):
        """Determine if able to select a button.

        Returns:pass
            bool: player able to select
        """
        return self._can_select

    @can_select.setter
    def can_select(self, can_select: bool):
        """Set self._can_select

        Args:
            can_select (bool): Check if element can be selected
        """
        self._can_select = can_select

    @property
    def selector_pos(self):
        """Get the selector's current x/y

        Returns:
            tuple(float, float): position of the selector
        """
        return (self._button_list[self._cur_selection].center_x,
                self._button_list[self._cur_selection].center_y * 0.78)
