import matplotlib.pyplot as plt
import mplfinance as mpf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter, AutoDateLocator
import tkinter as tk
from datetime import datetime, timedelta


class ChartManager:
    def __init__(self, frame):
        self.frame = frame
        self.figure, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)

        # Configure how many candles to show for each timeframe
        self.timeframe_candle_count = {
            '30m': 92,  # 48 hours worth of 30m candles
            '1h': 92,  # 4 days worth of 1h candles
            '4h': 84,  # 14 days worth of 4h candles
            '1d': 180  # 180 days worth of daily candles
        }

        self.timeframe_bar_width = {
            '30m': 0.02,  # About half an hour in days
            '1h': 0.04,   # About an hour in days
            '4h': 0.15,   # About 4 hours in days
            '1d': 0.8     # Most of a day
        }

        self.style = {
            'up_color': '#26a69a',
            'down_color': '#ef5350',
            'edge_color': 'black',
            'grid_color': '#2c2c2c',
            'bg_color': 'white'
        }

        # Configure the plot
        self.ax.set_facecolor(self.style['bg_color'])
        self.figure.patch.set_facecolor(self.style['bg_color'])
        self.ax.grid(True, color=self.style['grid_color'], linestyle='--', alpha=0.3)

    def update_chart(self, data, timeframe):
        self.ax.clear()

        # Get only the last N candles based on timeframe
        n_candles = self.timeframe_candle_count[timeframe]
        data = data.tail(n_candles)

        # Get bar width for current timeframe
        bar_width = self.timeframe_bar_width[timeframe]

        # Create candlestick chart
        up_candles = data[data['Close'] >= data['Open']]
        down_candles = data[data['Close'] < data['Open']]

        # Plot up candles
        self.ax.vlines(up_candles.index, up_candles['Low'], up_candles['High'],
                       color=self.style['up_color'], linewidth=1)
        self.ax.vlines(down_candles.index, down_candles['Low'], down_candles['High'],
                       color=self.style['down_color'], linewidth=1)

        # Plot candle bodies with adjusted width
        self.ax.bar(up_candles.index, up_candles['Close'] - up_candles['Open'],
                    bottom=up_candles['Open'], width=bar_width,
                    color=self.style['up_color'])
        self.ax.bar(down_candles.index, down_candles['Close'] - down_candles['Open'],
                    bottom=down_candles['Open'], width=bar_width,
                    color=self.style['down_color'])

        # Format x-axis to show appropriate number of ticks
        if timeframe in ['30m', '1h']:
            locator = AutoDateLocator(minticks=3, maxticks=7)
        else:
            locator = AutoDateLocator(minticks=5, maxticks=10)

        self.ax.xaxis.set_major_locator(locator)

        # Style the chart
        self.ax.set_facecolor(self.style['bg_color'])
        self.ax.grid(True, color=self.style['grid_color'], linestyle='--', alpha=0.3)

        # Format x-axis
        self.ax.set_xlabel('')

        # Format date/time based on timeframe
        if timeframe in ['30m', '1h']:
            # For shorter timeframes, show date and time
            plt.xticks(rotation=45)
            self.ax.xaxis.set_major_formatter(DateFormatter('%d %b \'%y %H:%M'))
        else:
            # For longer timeframes, show only date
            plt.xticks(rotation=45)
            self.ax.xaxis.set_major_formatter(DateFormatter('%d %b \'%y'))

        # Use AutoDateLocator for automatic date tick selection
        self.ax.xaxis.set_major_locator(AutoDateLocator())

        # Remove spines
        for spine in self.ax.spines.values():
            spine.set_color(self.style['grid_color'])
            spine.set_alpha(0.3)

        # Title with timeframe
        self.ax.set_title(f'BTC/USD - {timeframe}', color='black')

        # Adjust layout to prevent label cutoff
        plt.tight_layout()

        # Update the canvas
        self.canvas.draw()

    def pack(self):
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def destroy(self):
        plt.close(self.figure)