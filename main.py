# main.py

from src.gameloop import GameLoop
from src.ui.window import Window


def main():
    window = Window()
    game = GameLoop()
    game.run()


if __name__ == "__main__":
    main()
