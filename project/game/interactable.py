""" Map Interactions """
# TODO remove Threading because it won't do what is intended as this is a CPU bound problem
from concurrent.futures import ThreadPoolExecutor
from game import constants

class Interactable:
    """ In charge of map interaction

    Stereotype: Coordinator, Controller

    Attributes:
       self._player (sprite): the player
       self._can_interact (bool): Check if player can interact
       self._last_intersect_msg (int):
    """
    def __init__(self, tiled_object_list, player, map_height):
        """ Class Contructor

        Args:
            tiled_object_list (dict): the map objects
            player (sprite): The player
            map_height (int): The map height
        """
        def parse_box(interactable):
            """TODO

            Args:
                interactable ([type]): [description]

            Returns:
                [type]: [description]
            """
            begin_x = round(interactable.shape[0][0] * constants.TILE_SCALING)
            end_x = round(interactable.shape[1][0] * constants.TILE_SCALING)
            end_y = round(interactable.shape[0][1] * constants.TILE_SCALING) + map_height
            begin_y = round(interactable.shape[2][1] * constants.TILE_SCALING) + map_height
            return ((begin_x, end_x),
                    (begin_y, end_y),
                    (interactable.properties,))

        with ThreadPoolExecutor() as threader:
            self._interactable_ranges = tuple(threader.map(parse_box, tiled_object_list))

        self._player = player
        self._can_interact = False
        self._last_intersect_msg = 5

    def _mod_y(self, y_range):
        """TODO

        Args:
            y_range ([type]): [description]

        Returns:
            [type]: [description]
        """
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
        """TODO

        Args:
            x_range ([type]): [description]

        Returns:
            [type]: [description]
        """
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
        """TODO

        Args:
            interactable ([type]): [description]

        Returns:
            [type]: [description]
        """
        with ThreadPoolExecutor(max_workers=4) as threader:
            mod_x_future = threader.submit(self._mod_x, interactable[0])
            mod_y_future = threader.submit(self._mod_y, interactable[1])
            return (mod_x_future.result(),
                    mod_y_future.result(),
                    interactable[2])

    @staticmethod
    def _filter_active(interactable):
        """TODO

        Args:
            interactable ([type]): [description]

        Returns:
            [type]: [description]
        """
        # coll_side_x, begin_x, end_x; coll_side_y, begin_y, end_y
        return bool(interactable[0][1] <=
                    interactable[0][0] <=
                    interactable[0][2]

                    and interactable[1][1] <=
                    interactable[1][0] <=
                    interactable[1][2]
        )

    def update_interactable(self, delta_time = 1/60, force_check=False):
        """TODO

        Args:
            delta_time ([type], optional): [description]. Defaults to 1/60.
            force_check (bool, optional): [description]. Defaults to False.
        """
        if (
            self._player.change_x == 0 and self._player.change_y == 0
        ) and not force_check:
            return
        with ThreadPoolExecutor() as threader:
            cur_object_ranges = tuple(threader.map(
                self._add_modifiers,
                self._interactable_ranges))
        self._active_objects = tuple(filter(self._filter_active, cur_object_ranges))
        self._can_interact = (len(self._active_objects) > 0)
        if len(self._active_objects) > 1:
            if self._last_intersect_msg > 5:
                print('Warning: Detected multiple intersecting iteraction boxes')
                self._last_intersect_msg = 0
            self._last_intersect_msg += delta_time


    @property
    def can_interact(self):
        """ Get can_interact

        Returns:
            bool: check if can interact
        """
        return self._can_interact

    @property
    def interact_text(self):
        """ Get the get the text from the map objects

        Returns:
            str: the text to be displayed
        """
        return self._active_objects[0][2][0]['text']

    @property
    def interact_properties(self):
        """ Get the objects to interact with in the map

        Returns:
            dict: the objects. The values are strings
        """
        return self._active_objects[0][2][0]
