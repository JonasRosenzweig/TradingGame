import tkinter as tk
from utils.constants import *


class StartScreen:
    def __init__(self, root, game_instance):  # Add game_instance parameter
        self.root = root
        self.game_instance = game_instance  # Store the reference
        self.frame = tk.Frame(
            root,
            bg=BACKGROUND_COLOR,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT
        )

    def setup(self):
        # Center the title
        title_label = tk.Label(
            self.frame,
            text=GAME_TITLE,
            font=("Helvetica", 32, "bold"),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR
        )
        title_label.place(relx=0.5, rely=0.3, anchor="center")

        # Add start button
        start_button = tk.Button(
            self.frame,
            text="Start Game",
            font=("Helvetica", 16),
            command=self._start_game
        )
        start_button.place(relx=0.5, rely=0.5, anchor="center")

        # Add quit button
        quit_button = tk.Button(
            self.frame,
            text="Quit",
            font=("Helvetica", 16),
            command=self.root.quit
        )
        quit_button.place(relx=0.5, rely=0.6, anchor="center")

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()

    def _start_game(self):
        # Get reference to main game instance
        game = self.root.winfo_toplevel()
        self.game_instance.show_save_screen()