import tkinter as tk
from screens.start_screen import StartScreen
from utils.constants import *


class TradingGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(GAME_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        # Initialize screens
        self.start_screen = StartScreen(self.root)

        # Show start screen
        self.start_screen.setup()
        self.start_screen.show()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = TradingGame()
    game.run()