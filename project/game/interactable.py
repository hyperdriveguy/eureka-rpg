import arcade
from concurrent.futures import ThreadPoolExecutor
from game import constants
from game.utils import is_between

class Interactable:

    def __init__(self, tiled_object_list, player, map_height):
        def parse_box(interactable):
            begin_x = round(interactable.shape[0][0] * constants.TILE_SCALING)
            end_x = round(interactable.shape[1][0] * constants.TILE_SCALING)
            end_y = round(interactable.shape[0][1] * constants.TILE_SCALING) + map_height
            begin_y = round(interactable.shape[2][1] * constants.TILE_SCALING) + map_height
            return ((begin_x, end_x),
                    (begin_y, end_y),
                    (interactable.properties,))

        with ThreadPoolExecutor() as exec:
            self._interactable_ranges = tuple(exec.map(parse_box, tiled_object_list))

        self._player = player
        self._can_interact = False

    def _mod_y(self, y_range):
        begin_y, end_y = y_range
        coll_side_y = self._player.center_y
        if self._player.character_face_y == constants.FACE_UP:
            begin_y = y_range[0] - 10
            coll_side_y = self._player.top
        elif self._player.character_face_y == constants.FACE_DOWN:
            end_y = y_range[1] + 10
            coll_side_y = self._player.bottom
        return (coll_side_y, begin_y, end_y)

    def _mod_x(self, x_range):
        begin_x, end_x = x_range
        coll_side_x = self._player.center_x
        if self._player.character_face_x == constants.FACE_LEFT:
            end_x = x_range[1] + 10
            coll_side_x = self._player.left
        elif self._player.character_face_x ==  constants.FACE_RIGHT:
            begin_x = x_range[0] - 10
            coll_side_x = self._player.right
        return (coll_side_x, begin_x, end_x)

    def _add_modifiers(self, interactable):
        with ThreadPoolExecutor(max_workers=4) as exec:
            mod_x_future = exec.submit(self._mod_x, interactable[0])
            mod_y_future = exec.submit(self._mod_y, interactable[1])
            return (mod_x_future.result(),
                    mod_y_future.result(),
                    interactable[2])

    @staticmethod
    def _filter_active(interactable):
        # coll_side_x, begin_x, end_x; coll_side_y, begin_y, end_y
        if (is_between(interactable[0][0], interactable[0][1], interactable[0][2]) and
                is_between(interactable[1][0], interactable[1][1], interactable[1][2])):
            return True
        return False
    
    def update_interactable(self, force_check=False):
        if not (self._player.change_x == 0 and self._player.change_y == 0) or force_check:
            with ThreadPoolExecutor() as exec:
                cur_object_ranges = tuple(exec.map(
                    self._add_modifiers,
                    self._interactable_ranges))
            self._active_objects = tuple(filter(self._filter_active, cur_object_ranges))
            self._can_interact = (len(self._active_objects) > 0)
            if len(self._active_objects) > 1:
                print(('Warning: Detected multiple intersecting iteraction boxes'))
    
    @property
    def can_interact(self):
        return self._can_interact
    
    @property
    def interact_text(self):
        return self._active_objects[0][2][0]['text']
