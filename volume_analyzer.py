"""
Volume Analyzer - Phân tích volume và buy/sell pressure
Detects volume surges, buy/sell pressure, and volume profile
"""

import ccxt
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple

def fetch_recent_trades(symbol: str, limit: int = 500) -> pd.DataFrame:
    """
    Fetch recent trades to analyze buy/sell pressure
    
    Args:
        symbol: Trading pair
        limit: Number of recent trades
    
    Returns:
        DataFrame with trades data
    """
    exchange = ccxt.binance({
        'options': {'defaultType': 'future'},
        'enableRateLimit': True
    })
    
    try:
        trades = exchange.fetch_trades(symbol, limit=limit)
        df = pd.DataFrame(trades)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"[ERROR] Error fetching trades for {symbol}: {e}")
        return pd.DataFrame()

def calculate_buy_sell_pressure(symbol: str) -> Dict:
    """
    Tính tỷ lệ buy/sell pressure từ recent trades
    
    Returns:
        {
            'buy_volume': float,
            'sell_volume': float,
            'buy_sell_ratio': float,
            'sell_pressure_pct': float,
            'message': str
        }
    """
    try:
        df = fetch_recent_trades(symbol, limit=500)
        
        if df.empty:
            return {'error': 'Không có dữ liệu trades'}
        
        # Classify trades as buy or sell based on side
        # In Binance, 'side' indicates taker side
        buy_trades = df[df['side'] == 'buy']
        sell_trades = df[df['side'] == 'sell']
        
        buy_volume = (buy_trades['price'] * buy_trades['amount']).sum()
        sell_volume = (sell_trades['price'] * sell_trades['amount']).sum()
        
        total_volume = buy_volume + sell_volume
        
        if total_volume == 0:
            return {'error': 'Volume = 0'}
        
        buy_sell_ratio = buy_volume / sell_volume if sell_volume > 0 else float('inf')
        sell_pressure_pct = (sell_volume / total_volume) * 100
        buy_pressure_pct = (buy_volume / total_volume) * 100
        
        # Generate message
        if sell_pressure_pct > 70:
            message = f'🔴 ÁP LỰC BÁN CAO! Sell: {sell_pressure_pct:.1f}% vs Buy: {buy_pressure_pct:.1f}%'
            severity = 'critical'
        elif sell_pressure_pct > 60:
            message = f'⚠️ Sell pressure cao: {sell_pressure_pct:.1f}%'
            severity = 'warning'
        elif buy_pressure_pct > 60:
            message = f'✅ Buy pressure mạnh: {buy_pressure_pct:.1f}%'
            severity = 'info'
        else:
            message = f'📊 Cân bằng: Buy {buy_pressure_pct:.1f}% - Sell {sell_pressure_pct:.1f}%'
            severity = 'info'
        
        return {
            'buy_volume': buy_volume,
            'sell_volume': sell_volume,
            'buy_sell_ratio': buy_sell_ratio,
            'sell_pressure_pct': sell_pressure_pct,
            'buy_pressure_pct': buy_pressure_pct,
            'severity': severity,
            'message': message
        }
        
    except Exception as e:
        print(f"[ERROR] Failed to calculate buy/sell pressure for {symbol}: {e}")
        return {'error': str(e)}

def analyze_volume_trend(symbol: str) -> Dict:
    """
    Phân tích xu hướng volume (tăng/giảm)
    
    Returns:
        {
            'trend': 'increasing' | 'decreasing' | 'stable',
            'volume_change_pct': float,
            'message': str
        }
    """
    try:
        # Import from mm_detector
        from mm_detector import fetch_klines
        
        df = fetch_klines(symbol, interval='5m', limit=24)
        
        if df.empty or len(df) < 12:
            return {'error': 'Không đủ dữ liệu'}
        
        # Compare recent volume vs older volume
        recent_volume = df.iloc[-6:]['volume'].mean()  # Last 30 minutes
        older_volume = df.iloc[-12:-6]['volume'].mean()  # Previous 30 minutes
        
        volume_change_pct = ((recent_volume - older_volume) / older_volume) * 100 if older_volume > 0 else 0
        
        if volume_change_pct > 50:
            trend = 'increasing'
            message = f'📈 Volume đang tăng mạnh (+{volume_change_pct:.1f}%)'
        elif volume_change_pct < -30:
            trend = 'decreasing'
            message = f'📉 Volume đang giảm ({volume_change_pct:.1f}%)'
        else:
            trend = 'stable'
            message = f'📊 Volume ổn định ({volume_change_pct:+.1f}%)'
        
        return {
            'trend': trend,
            'volume_change_pct': volume_change_pct,
            'recent_volume': recent_volume,
            'older_volume': older_volume,
            'message': message
        }
        
    except Exception as e:
        print(f"[ERROR] Failed to analyze volume trend for {symbol}: {e}")
        return {'error': str(e)}
