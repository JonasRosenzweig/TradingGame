# screens/save_screen.py
import tkinter as tk
from tkinter import simpledialog
from utils.constants import *
from utils.save_manager import SaveManager


class SaveScreen:
    def __init__(self, root, game_instance):  # Add game_instance parameter
        self.root = root
        self.game_instance = game_instance  # Store the reference
        self.frame = tk.Frame(
            root,
            bg=BACKGROUND_COLOR,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT
        )
        self.saves = SaveManager.load_saves()
        self.save_buttons = []

    def setup(self):
        # Title
        title_label = tk.Label(
            self.frame,
            text="Select Save File",
            font=("Helvetica", 24, "bold"),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR
        )
        title_label.place(relx=0.5, rely=0.2, anchor="center")

        # Create save slot buttons
        for i in range(SaveManager.MAX_SAVES):
            save_data = self.saves[f"save_{i + 1}"]
            button_text = f"Save {i + 1}: {save_data['name'] or 'Empty'}"

            button = tk.Button(
                self.frame,
                text=button_text,
                font=("Helvetica", 16),
                width=20,
                command=lambda slot=i + 1: self._handle_save_selection(slot)
            )
            button.place(relx=0.5, rely=0.4 + (i * 0.15), anchor="center")
            self.save_buttons.append(button)

        # Back button
        back_button = tk.Button(
            self.frame,
            text="Back",
            font=("Helvetica", 12),
            command=self._go_back
        )
        back_button.place(relx=0.1, rely=0.9, anchor="center")

    def _handle_save_selection(self, slot):
        save_data = self.saves[f"save_{slot}"]

        if save_data["name"] is None:
            player_name = simpledialog.askstring(
                "New Game",
                "Enter your name:",
                parent=self.root
            )

            if player_name:
                SaveManager.create_new_save(slot, player_name)
                self.saves = SaveManager.load_saves()  # Refresh saves
                # Remove the _update_button_texts call from here
                self.game_instance.start_game(self.saves[f"save_{slot}"])
        else:
            self.game_instance.start_game(save_data)

    def _update_button_texts(self):
        for i, button in enumerate(self.save_buttons):
            save_data = self.saves[f"save_{i + 1}"]
            button.config(text=f"Save {i + 1}: {save_data['name'] or 'Empty'}")

    def _go_back(self):
        self.hide()
        self.game_instance.show_start_screen()
        # We'll implement this when we update the main game class

    def show(self):
        # Reload saves and recreate buttons every time we show the screen
        self.saves = SaveManager.load_saves()
        self.frame.destroy()  # Destroy old frame
        self.frame = tk.Frame(  # Create new frame
            self.root,
            bg=BACKGROUND_COLOR,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT
        )
        self.setup()  # Recreate all widgets
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()