import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.price_manager import PriceManager


def test_price_manager():
    pm = PriceManager()

    # Try to load existing data
    if not pm.load_data():
        print("Fetching new data...")
        success = pm.fetch_historical_data()
        if success:
            pm.save_data()

    # Test different timeframes
    for timeframe in ['30m', '1h', '4h', '1d']:
        data = pm.get_candles(timeframe)
        print(f"\n{timeframe} candles:")
        print(f"Number of candles: {len(data)}")
        print("Latest candle:")
        print(data.tail(1))

    print(f"\nLatest Bitcoin price: ${pm.get_latest_price():.2f}")


if __name__ == "__main__":
    test_price_manager()