# screens/game_screen.py
import tkinter as tk
from tkinter import messagebox
from utils.constants import *
from utils.constants import *
from utils.save_manager import SaveManager
from utils.chart_manager import ChartManager
from utils.price_manager import PriceManager


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
        self.price_manager = PriceManager()
        self.current_timeframe = '1h'  # Default timeframe

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

        # Create chart frame
        chart_frame = tk.Frame(
            self.frame,
            bg="white",
            width=WINDOW_WIDTH - CONTROL_PANEL_WIDTH - 40,
            height=WINDOW_HEIGHT - 150
        )
        chart_frame.place(x=20, y=100)
        chart_frame.pack_propagate(False)

        # Add the control buttons
        self._create_trading_controls()

        # add controls buttons
        self._create_control_buttons()

        timeframe_frame = tk.Frame(
            self.frame,
            bg=BACKGROUND_COLOR,
            padx=10,
            pady=5
        )
        timeframe_frame.place(relx=0.5, y=40, anchor="n")

        # Add timeframe buttons
        timeframes = ['30m', '1h', '4h', '1d']
        for tf in timeframes:
            btn = tk.Button(
                timeframe_frame,
                text=tf,
                command=lambda t=tf: self._change_timeframe(t),
                width=6
            )
            btn.pack(side=tk.LEFT, padx=5)

        # Create chart frame with adjusted width for control panel
        chart_frame = tk.Frame(
            self.frame,
            bg="white",
            width=WINDOW_WIDTH - CONTROL_PANEL_WIDTH - 40,  # Adjusted width calculation
            height=WINDOW_HEIGHT - 150
        )
        chart_frame.place(x=20, y=100)
        chart_frame.pack_propagate(False)

        # Create trading controls
        self._create_trading_controls()

        # Initialize price data and chart
        self.price_manager.fetch_historical_data()
        self.chart_manager = ChartManager(chart_frame)
        self._update_chart()
        self.chart_manager.pack()

        # Start periodic updates
        self._schedule_price_update()

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        if hasattr(self, 'chart_manager'):
            self.chart_manager.destroy()
        self.frame.pack_forget()

    def _change_timeframe(self, timeframe):
        self.current_timeframe = timeframe
        self._update_chart()

    def _update_chart(self):
        data = self.price_manager.get_candles(self.current_timeframe)
        self.chart_manager.update_chart(data, self.current_timeframe)

    def _schedule_price_update(self):
        # Update prices every minute
        self._update_chart()
        self.frame.after(60000, self._schedule_price_update)

    def update_account_value(self, new_value):
        self.account_label.config(text=f"Account: ${new_value:.2f}")

    def _create_trading_controls(self):
        # Control panel frame on the right
        control_panel = tk.Frame(
            self.frame,
            bg=BACKGROUND_COLOR,
            width=CONTROL_PANEL_WIDTH,
            height=WINDOW_HEIGHT - 150
        )
        control_panel.place(x=WINDOW_WIDTH - CONTROL_PANEL_WIDTH - 20, y=100)
        control_panel.pack_propagate(False)

        # Style configuration for buttons
        button_style = {
            'width': 6,  # Reduced width further
            'font': ('Helvetica', 8),  # Smaller font
            'pady': 2
        }

        # Spot trading section
        spot_frame = tk.LabelFrame(
            control_panel,
            text="Spot",  # Shortened labels
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            padx=2,
            pady=2
        )
        spot_frame.pack(fill='x', padx=1, pady=1)

        tk.Button(spot_frame, text="Buy", **button_style).pack(pady=1)
        tk.Button(spot_frame, text="Sell", **button_style).pack(pady=1)

        # Margin trading section
        margin_frame = tk.LabelFrame(
            control_panel,
            text="Margin",
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            padx=2,
            pady=2
        )
        margin_frame.pack(fill='x', padx=1, pady=1)

        tk.Button(margin_frame, text="1x", **button_style).pack(pady=1)  # Shortened text

        # Limit orders section
        limit_frame = tk.LabelFrame(
            control_panel,
            text="Limit",
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            padx=2,
            pady=2
        )
        limit_frame.pack(fill='x', padx=1, pady=1)

        tk.Button(limit_frame, text="Buy", **button_style).pack(pady=1)  # Shortened text
        tk.Button(limit_frame, text="Sell", **button_style).pack(pady=1)  # Shortened text

        # Order creator section
        order_frame = tk.LabelFrame(
            control_panel,
            text="Create",
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            padx=2,
            pady=2
        )
        order_frame.pack(fill='x', padx=1, pady=1)

        tk.Button(order_frame, text="Create", **button_style).pack(pady=1)  # Shortened text

    def _save_game(self):
        # Get the save slot from player data
        save_slot = self.player_data.get('slot')
        if save_slot:
            SaveManager.update_save(save_slot, self.player_data)
            # Maybe add a small popup to confirm save
            tk.messagebox.showinfo("Success", "Game saved successfully!")

    def _return_to_menu(self):
        if tk.messagebox.askyesno("Return to Menu", "Are you sure? Don't forget to save your progress!"):
            self.hide()
            self.game_instance.show_start_screen()

    def _quit_game(self):
        if tk.messagebox.askyesno("Quit Game", "Save and quit?"):
            self._save_game()
            self.root.quit()

    def _create_control_buttons(self):
        # Control buttons frame (top right)
        control_frame = tk.Frame(
            self.frame,
            bg=BACKGROUND_COLOR,
            padx=10,
            pady=5
        )
        control_frame.place(relx=1, y=10, anchor="ne")

        # Save button
        save_button = tk.Button(
            control_frame,
            text="Save",
            command=self._save_game,
            width=10
        )
        save_button.pack(side=tk.LEFT, padx=5)

        # Main Menu button
        menu_button = tk.Button(
            control_frame,
            text="Main Menu",
            command=self._return_to_menu,
            width=10
        )
        menu_button.pack(side=tk.LEFT, padx=5)

        # Quit button
        quit_button = tk.Button(
            control_frame,
            text="Quit",
            command=self._quit_game,
            width=10
        )
        quit_button.pack(side=tk.LEFT, padx=5)

