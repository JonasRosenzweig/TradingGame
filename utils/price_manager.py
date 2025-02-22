# utils/price_manager.py
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

class PriceManager:
    def __init__(self):
        self.symbol = "BTC-USD"
        self.raw_data = None
        self.timeframes = {
            '30m': 30,
            '1h': 60,
            '4h': 240,
            '1d': 1440
        }
        self.data_dir = 'data'
        os.makedirs(self.data_dir, exist_ok=True)
        self.last_price = None
        self.current_price = None
        self.update_interval = 30  # 30 seconds to avoid rate limits

    def fetch_historical_data(self):
        """
        Fetches 60 days of historical data for Bitcoin (Yahoo's limit for 30m data)
        Returns DataFrame with OHLCV data
        """
        try:
            btc = yf.Ticker(self.symbol)
            # Get 60 days of 30-minute data (Yahoo's limit)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=60)

            self.raw_data = btc.history(
                start=start_date,
                end=end_date,
                interval="30m"
            )

            # Clean the data
            self.raw_data = self.raw_data[['Open', 'High', 'Low', 'Close', 'Volume']]
            self.raw_data = self.raw_data.dropna()

            # Ensure index is datetime
            self.raw_data.index = pd.to_datetime(self.raw_data.index)

            print(f"Fetched {len(self.raw_data)} data points")
            return True

        except Exception as e:
            print(f"Error fetching data: {e}")
            return False

    def get_candles(self, timeframe):
        """
        Returns OHLCV data for specified timeframe
        timeframe: '30m', '1h', '4h', or '1d'
        """
        if timeframe not in self.timeframes:
            raise ValueError(f"Invalid timeframe. Must be one of {list(self.timeframes.keys())}")

        if self.raw_data is None:
            raise ValueError("No data available. Call fetch_historical_data first.")

        # For 30m, just return the raw data
        if timeframe == '30m':
            return self.raw_data

        # For other timeframes, resample the data
        minutes = self.timeframes[timeframe]
        resampled = self.raw_data.resample(f'{minutes}min').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        })

        return resampled.dropna()

    def get_latest_price(self):
        """Returns the most recent closing price"""
        if self.raw_data is None:
            raise ValueError("No data available. Call fetch_historical_data first.")
        return self.raw_data['Close'].iloc[-1]

    def save_data(self):
        """Saves the data to a file to avoid frequent API calls"""
        if self.raw_data is not None:
            filepath = os.path.join(self.data_dir, 'btc_price_history.pkl')
            self.raw_data.to_pickle(filepath)

    def load_data(self):
        """Loads the data from file if available"""
        try:
            filepath = os.path.join(self.data_dir, 'btc_price_history.pkl')
            self.raw_data = pd.read_pickle(filepath)

            # Ensure index is datetime
            self.raw_data.index = pd.to_datetime(self.raw_data.index)

            # Check if data is outdated (more than 1 hour old)
            last_timestamp = self.raw_data.index[-1]
            if datetime.now() - last_timestamp > timedelta(hours=1):
                return False
            return True
        except:
            return False

    def get_price_change(self):
        """Returns tuple of (price, is_increase)"""
        if self.last_price is None or self.current_price is None:
            return (self.current_price, None)
        return (self.current_price, self.current_price > self.last_price)

    def update_current_price(self):
        """Updates current price and returns True if successful"""
        try:
            btc = yf.Ticker(self.symbol)
            new_price = btc.history(period='1d', interval='1m').iloc[-1]['Close']

            self.last_price = self.current_price
            self.current_price = new_price
            return True
        except Exception as e:
            print(f"Error updating price: {e}")
            return False
