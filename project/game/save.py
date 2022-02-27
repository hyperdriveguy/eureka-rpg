""" Save game progress """

class Save():
    """ Responsible for saving the game and saving won battles so they can't be replayed after switching between maps.

    Stereotype: Information Holder
    """
    def __init__(self, path):
        """Class Constructor

        Args:
        """
        self._path = path

    def battle_complete(self, cur_battle):
        """ Append each line of the file to the list

            Return (bool): True if battle complete
        """
        with open(self._path, "rt") as file:
            for line in file:
                if cur_battle == line.strip("\n"):
                    return True
        return False



    def write_to_file(self, enemy_name):
        """ Append the battle that was won to the file
        """
        with open(self._path, "a") as file:
            print(enemy_name, file=file)

    def clear_file(self):
        """ Call when player dies to clear the file
        """
        with open(self._path, "w") as file:
            file.write("")
