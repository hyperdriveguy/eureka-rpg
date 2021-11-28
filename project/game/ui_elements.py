import arcade

class Button(arcade.SpriteList):
    
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
        super().__init__()
        
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

class Selector:
    
    def __init__(self, *buttons, orient='main'):
        self._button_list = arcade.SpriteList()
        for button in buttons:
            self._button_list.extend(button)
        self._cur_selection = 0
        
        self._selector_list = arcade.ShapeElementList()
        self._add_selector()
        self._can_select = False

    def _add_selector(self):
        self._selection_box = arcade.create_rectangle(
            self._button_list[self._cur_selection].center_x,
            self._button_list[self._cur_selection].center_y * 0.78,
            self._button_list[self._cur_selection].width *1.1,
            self._button_list[self._cur_selection].height * 0.8,
            arcade.color.BLACK,
            border_width=3,
            filled=False
        )
        self._selector_list.append(self._selection_box)
    
    def next_button(self):
        self._cur_selection += 1
        if self._cur_selection >= len(self._button_list):
            self._cur_selection = 0
        self._update_selector()
    
    def prev_button(self):
        self._cur_selection -= 1
        if self._cur_selection < 0:
            self._cur_selection = len(self._button_list) - 1
        self._update_selector()
    
    def _update_selector(self):
        self._selector_list.remove(self._selection_box)
        self._add_selector()
    
    def draw(self):
        self._button_list.draw()
        if self._can_select:
            self._selector_list.draw()
        
        
    @property
    def can_select(self):
        return self._can_select
    
    @can_select.setter
    def can_select(self, can_select: bool):
        self._can_select = can_select
