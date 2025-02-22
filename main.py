import tkinter as tk
from screens.start_screen import StartScreen
from screens.save_screen import SaveScreen
from utils.constants import *


class TradingGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(GAME_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        # Initialize screens - pass self as game_instance
        self.start_screen = StartScreen(self.root, self)
        self.save_screen = SaveScreen(self.root, self)  # Don't forget to update SaveScreen similarly

        # Show start screen
        self.start_screen.setup()
        self.start_screen.show()

    def show_save_screen(self):
        self.start_screen.hide()
        self.save_screen.setup()
        self.save_screen.show()

    def show_start_screen(self):
        self.save_screen.hide()
        self.start_screen.show()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = TradingGame()
    game.run()