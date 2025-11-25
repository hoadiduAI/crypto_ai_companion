import ccxt
import pandas as pd

def test_ccxt_ratio():
    try:
        exchange = ccxt.binance({'options': {'defaultType': 'future'}})
        # Fetch Long/Short Ratio
        # CCXT unifies this usually under fetch_funding_rate_history or similar, but L/S ratio is specific.
        # We might need to call the implicit API method.
        
        # publicGetFuturesDataGlobalLongShortAccountRatio
        # params: symbol, period, limit
        
        data = exchange.fapiPublic_get_toplongshortaccountratio({
            'symbol': 'BTCUSDT',
            'period': '5m',
            'limit': 1
        })
        print("Response:", data)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ccxt_ratio()
