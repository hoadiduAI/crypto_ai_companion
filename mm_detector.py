"""
Market Manipulation Detector
Detects Ghost Towns, Fake Pumps, Sharp Price Movements, and Volume Surges
"""

import ccxt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional

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

def fetch_klines(symbol: str, interval: str = '5m', limit: int = 50) -> pd.DataFrame:
    """
    Fetch candlestick data for price action analysis
    
    Args:
        symbol: Trading pair (e.g., 'BTC/USDT:USDT')
        interval: Timeframe ('1m', '5m', '15m', '1h')
        limit: Number of candles
    
    Returns:
        DataFrame with OHLCV data
    """
    exchange = ccxt.binance({
        'options': {'defaultType': 'future'},
        'enableRateLimit': True
    })
    
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, interval, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"[ERROR] Error fetching klines for {symbol}: {e}")
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

def detect_fake_pumps(df, min_change=15, max_volume_ratio=1.0):
    """
    Detect Fake Pumps: High price change but low/normal volume
    
    Args:
        min_change: Minimum price change % (default 15%)
        max_volume_ratio: Max volume ratio vs median (1.0 = normal volume)
    """
    if df.empty:
        return pd.DataFrame()
    
    # Calculate median volume
    median_volume = df['Volume'].median()
    
    fake_pumps = df[
        (df['Change'] > min_change) & 
        (df['Volume'] < median_volume * max_volume_ratio)
    ].copy()
    
    fake_pumps['Volume_Ratio'] = fake_pumps['Volume'] / median_volume
    
    return fake_pumps.sort_values('Change', ascending=False)

def detect_sharp_price_drop(symbol: str, threshold: float = 10, timeframe: int = 15) -> Dict:
    """
    Phát hiện giá giảm mạnh >10% trong 15 phút
    
    Args:
        symbol: Trading pair
        threshold: Price drop threshold % (default 10%)
        timeframe: Time window in minutes (default 15)
    
    Returns:
        {
            'detected': bool,
            'severity': 'critical' | 'warning' | 'info',
            'price_change': float,
            'volume_ratio': float,
            'is_real_dump': bool,
            'message': str
        }
    """
    try:
        # Fetch 5-minute candles for last hour
        df = fetch_klines(symbol, interval='5m', limit=20)
        
        if df.empty or len(df) < 4:
            return {'detected': False, 'message': 'Không đủ dữ liệu'}
        
        # Calculate price change in last 15 minutes (3 candles of 5m)
        current_price = df.iloc[-1]['close']
        price_15m_ago = df.iloc[-4]['close']
        price_change_pct = ((current_price - price_15m_ago) / price_15m_ago) * 100
        
        # Calculate volume ratio (last 15min vs previous 45min)
        volume_last_15m = df.iloc[-3:]['volume'].sum()
        volume_prev_45m = df.iloc[-12:-3]['volume'].sum()
        volume_ratio = volume_last_15m / (volume_prev_45m / 3) if volume_prev_45m > 0 else 0
        
        # Detection logic
        if price_change_pct >= -threshold:
            return {'detected': False, 'message': 'Giá không giảm đáng kể'}
        
        # Determine if it's a real dump (high volume)
        is_real_dump = volume_ratio > 1.5
        
        detected = True
        severity = 'info'
        message = ''
        
        # Critical: Giá giảm >15% + volume cao
        if price_change_pct <= -15 and is_real_dump:
            severity = 'critical'
            message = f'🚨 DUMP MẠNH! Giá giảm {abs(price_change_pct):.1f}% với volume cao ({volume_ratio:.1f}x)'
        
        # Warning: Giá giảm 10-15%
        elif price_change_pct <= -10:
            severity = 'warning'
            message = f'⚠️ Giá giảm {abs(price_change_pct):.1f}% trong 15 phút'
            if is_real_dump:
                message += ' (volume cao - dump thật)'
            else:
                message += ' (volume thấp - có thể phục hồi)'
        
        return {
            'detected': detected,
            'severity': severity,
            'price_change': price_change_pct,
            'volume_ratio': volume_ratio,
            'is_real_dump': is_real_dump,
            'current_price': current_price,
            'message': message
        }
        
    except Exception as e:
        print(f"[ERROR] Failed to detect sharp price drop for {symbol}: {e}")
        return {'detected': False, 'error': str(e)}

def detect_sharp_price_pump(symbol: str, threshold: float = 15, timeframe: int = 15) -> Dict:
    """
    Phát hiện giá tăng mạnh >15% trong 15 phút
    Kiểm tra volume để phân biệt pump thật vs fake pump
    
    Args:
        symbol: Trading pair
        threshold: Price pump threshold % (default 15%)
        timeframe: Time window in minutes (default 15)
    
    Returns:
        {
            'detected': bool,
            'severity': 'critical' | 'warning' | 'info',
            'price_change': float,
            'volume_ratio': float,
            'is_real_pump': bool,
            'message': str
        }
    """
    try:
        # Fetch 5-minute candles
        df = fetch_klines(symbol, interval='5m', limit=20)
        
        if df.empty or len(df) < 4:
            return {'detected': False, 'message': 'Không đủ dữ liệu'}
        
        # Calculate price change in last 15 minutes
        current_price = df.iloc[-1]['close']
        price_15m_ago = df.iloc[-4]['close']
        price_change_pct = ((current_price - price_15m_ago) / price_15m_ago) * 100
        
        # Calculate volume ratio
        volume_last_15m = df.iloc[-3:]['volume'].sum()
        volume_prev_45m = df.iloc[-12:-3]['volume'].sum()
        volume_ratio = volume_last_15m / (volume_prev_45m / 3) if volume_prev_45m > 0 else 0
        
        # Detection logic
        if price_change_pct <= threshold:
            return {'detected': False, 'message': 'Giá không tăng đáng kể'}
        
        # Determine if it's a real pump (volume >150% average)
        is_real_pump = volume_ratio > 1.5
        
        detected = True
        severity = 'info'
        message = ''
        
        # Real pump: High volume
        if is_real_pump:
            severity = 'warning'
            message = f'🚀 PUMP THẬT! Giá tăng {price_change_pct:.1f}% với volume cao ({volume_ratio:.1f}x)'
        
        # Fake pump: Low volume
        else:
            severity = 'info'
            message = f'⚠️ FAKE PUMP! Giá tăng {price_change_pct:.1f}% nhưng volume thấp ({volume_ratio:.1f}x) - Cẩn thận bull trap!'
        
        return {
            'detected': detected,
            'severity': severity,
            'price_change': price_change_pct,
            'volume_ratio': volume_ratio,
            'is_real_pump': is_real_pump,
            'current_price': current_price,
            'message': message
        }
        
    except Exception as e:
        print(f"[ERROR] Failed to detect sharp price pump for {symbol}: {e}")
        return {'detected': False, 'error': str(e)}

def detect_volume_surge(symbol: str, threshold: float = 2.0) -> Dict:
    """
    Phát hiện volume tăng đột biến >200% so với trung bình
    
    Args:
        symbol: Trading pair
        threshold: Volume surge threshold (2.0 = 200%)
    
    Returns:
        {
            'detected': bool,
            'severity': str,
            'current_volume': float,
            'avg_volume': float,
            'volume_ratio': float,
            'message': str
        }
    """
    try:
        # Fetch 5-minute candles for last 2 hours
        df = fetch_klines(symbol, interval='5m', limit=24)
        
        if df.empty or len(df) < 12:
            return {'detected': False, 'message': 'Không đủ dữ liệu'}
        
        # Current volume (last 5 minutes)
        current_volume = df.iloc[-1]['volume']
        
        # Average volume (previous 1 hour = 12 candles)
        avg_volume = df.iloc[-13:-1]['volume'].mean()
        
        # Volume ratio
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0
        
        if volume_ratio <= threshold:
            return {'detected': False, 'message': 'Volume bình thường'}
        
        detected = True
        severity = 'info'
        message = ''
        
        # Critical: Volume tăng >400%
        if volume_ratio > 4.0:
            severity = 'critical'
            message = f'🔥 VOLUME SURGE CỰC MẠNH! Tăng {volume_ratio:.1f}x trung bình'
        
        # Warning: Volume tăng >300%
        elif volume_ratio > 3.0:
            severity = 'warning'
            message = f'📊 Volume tăng mạnh: {volume_ratio:.1f}x trung bình'
        
        # Info: Volume tăng >200%
        else:
            severity = 'info'
            message = f'📈 Volume tăng: {volume_ratio:.1f}x trung bình'
        
        return {
            'detected': detected,
            'severity': severity,
            'current_volume': current_volume,
            'avg_volume': avg_volume,
            'volume_ratio': volume_ratio,
            'message': message
        }
        
    except Exception as e:
        print(f"[ERROR] Failed to detect volume surge for {symbol}: {e}")
        return {'detected': False, 'error': str(e)}

def detect_volatility_spike(symbol: str, threshold: float = 3.0) -> Dict:
    """
    Phát hiện volatility tăng đột biến
    
    Args:
        symbol: Trading pair
        threshold: Volatility spike threshold (3.0 = 3x normal)
    
    Returns:
        {
            'detected': bool,
            'current_volatility': float,
            'avg_volatility': float,
            'volatility_ratio': float,
            'message': str
        }
    """
    try:
        # Fetch 5-minute candles
        df = fetch_klines(symbol, interval='5m', limit=24)
        
        if df.empty or len(df) < 12:
            return {'detected': False, 'message': 'Không đủ dữ liệu'}
        
        # Calculate volatility (high-low range as % of close)
        df['volatility'] = ((df['high'] - df['low']) / df['close']) * 100
        
        # Current volatility (last candle)
        current_volatility = df.iloc[-1]['volatility']
        
        # Average volatility (previous 1 hour)
        avg_volatility = df.iloc[-13:-1]['volatility'].mean()
        
        # Volatility ratio
        volatility_ratio = current_volatility / avg_volatility if avg_volatility > 0 else 0
        
        if volatility_ratio <= threshold:
            return {'detected': False, 'message': 'Volatility bình thường'}
        
        detected = True
        message = f'⚡ Volatility tăng {volatility_ratio:.1f}x - Thị trường bất ổn!'
        
        return {
            'detected': detected,
            'current_volatility': current_volatility,
            'avg_volatility': avg_volatility,
            'volatility_ratio': volatility_ratio,
            'message': message
        }
        
    except Exception as e:
        print(f"[ERROR] Failed to detect volatility spike for {symbol}: {e}")
        return {'detected': False, 'error': str(e)}

