import requests
import pandas as pd

def test_binance_ratio():
    try:
        # Top Trader Long/Short Ratio (Accounts)
        url = "https://fapi.binance.com/fapi/v1/topLongShortAccountRatio"
        params = {
            'symbol': 'BTCUSDT',
            'period': '5m',
            'limit': 1
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        print("Response:", data)
        
        if isinstance(data, list) and len(data) > 0:
            ratio = float(data[0]['longShortRatio'])
            print(f"BTCUSDT Ratio: {ratio}")
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_binance_ratio()
