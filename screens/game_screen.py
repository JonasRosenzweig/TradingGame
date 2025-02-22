# screens/game_screen.py
import tkinter as tk
from utils.constants import *


class GameScreen:
    def __init__(self, root, game_instance):
        self.root = root
        self.game_instance = game_instance
        self.frame = tk.Frame(
            root,
            bg=BACKGROUND_COLOR,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT
        )
        self.player_data = None  # Will be set when loading a save

    def setup(self, save_data):
        self.player_data = save_data

        # Player info panel (top left)
        info_frame = tk.Frame(
            self.frame,
            bg=BACKGROUND_COLOR,
            padx=10,
            pady=5
        )
        info_frame.place(x=10, y=10)

        # Player name
        name_label = tk.Label(
            info_frame,
            text=f"Player: {self.player_data['name']}",
            font=("Helvetica", 12),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR
        )
        name_label.pack(anchor="w")

        # Account value
        self.account_label = tk.Label(
            info_frame,
            text=f"Account: ${self.player_data['data']['money']:.2f}",
            font=("Helvetica", 12),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR
        )
        self.account_label.pack(anchor="w")

        # Main trading area (empty box for now)
        trading_frame = tk.Frame(
            self.frame,
            bg="white",
            width=WINDOW_WIDTH - 40,  # 20px padding on each side
            height=WINDOW_HEIGHT - 100  # Space for top info
        )
        trading_frame.place(x=20, y=80)
        # Prevent frame from shrinking
        trading_frame.pack_propagate(False)

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()

    def update_account_value(self, new_value):
        self.account_label.config(text=f"Account: ${new_value:.2f}")