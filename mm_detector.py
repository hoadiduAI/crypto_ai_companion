import ccxt
import pandas as pd
import time

def fetch_binance_data():
    """Fetches ticker data from Binance Futures"""
    exchange = ccxt.binance({
        'options': {'defaultType': 'future'},
        'enableRateLimit': True
    })
    try:
        tickers = exchange.fetch_tickers()
        data = []
        for symbol, ticker in tickers.items():
            if '/USDT' in symbol and ':USDT' in symbol:
                price = ticker.get('last', 0)
                volume_usdt = ticker.get('quoteVolume', 0)
                percentage = ticker.get('percentage', 0)
                
                if price is None or volume_usdt is None:
                    continue
                    
                data.append({
                    'Symbol': symbol.replace(':USDT', ''),
                    'Price': price,
                    'Volume': volume_usdt,
                    'Change': percentage
                })
        return pd.DataFrame(data)
    except Exception as e:
        print(f"[ERROR] Error fetching data: {e}")
        return pd.DataFrame()

def detect_ghost_towns(df, min_price=0.5, max_volume=10_000_000):
    """Detect Ghost Towns: High price but low volume"""
    if df.empty:
        return pd.DataFrame()
    
    ghost_towns = df[
        (df['Price'] > min_price) & 
        (df['Volume'] < max_volume)
    ].copy()
    
    return ghost_towns.sort_values('Volume')

def detect_fake_pumps(df, min_change=10, max_volume=10_000_000):
    """Detect Fake Pumps: High price change but low volume"""
    if df.empty:
        return pd.DataFrame()
    
    fake_pumps = df[
        (df['Change'] > min_change) & 
        (df['Volume'] < max_volume)
    ].copy()
    
    return fake_pumps.sort_values('Change', ascending=False)
