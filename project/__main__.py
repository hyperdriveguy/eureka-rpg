from arcade import run

from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_NAME
from game.main_window import MainWindow

def main():
    game = MainWindow(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_NAME)
    game.setup()
    run()

if __name__ == "__main__":
    main()