    """ Save game progress """

class Save():
    """ Responsible for saving the game and saving won battles so they can't be replayed after switching between maps.

    Stereotype: Information Holder
    """
    def __init__(self, battles_won: list, path):
        """Class Constructor

        Args:
            battles_won (list): The list of battles that have been won
        """
        self._battles_won = battles_won
        self._path = path

    def file_to_list(self):
        """ Append each line of the file to the list
        """
        with open(self._path, "rt") as file:
            for line in file:
                self._battles_won.append(line)

    def append_to_file(self):
        """ Append battle won to the file
        """