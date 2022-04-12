"""Module to run the game.
"""

from arcade import run

from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_NAME
from game.main_window import MainWindow

def main():
    """Main function for playing the game.

    This function passes the needed constants to set up the game window.
    """
    game = MainWindow(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_NAME)
    game.setup()
    game.set_vsync(True)
    run()

if __name__ == "__main__":
    main()
