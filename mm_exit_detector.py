"""
MM Exit Detector - Phát hiện tín hiệu Market Maker rút lui
Detects when MM is preparing to exit: wall removal, liquidity drain, sell pressure
"""

import ccxt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

class MMExitDetector:
    def __init__(self, exchange: ccxt.Exchange):
        self.exchange = exchange
        self.orderbook_history = {}  # {symbol: [(timestamp, bid_support, ask_resistance)]}
        self.baseline_window = 30  # minutes
        
    def calculate_bid_support(self, orderbook: dict, depth_usd: float = 100000) -> float:
        """
        Tính tổng bid support trong khoảng depth_usd
        Returns: Tổng số USD bid orders trong khoảng giá depth
        """
        bids = orderbook['bids']
        total_support = 0
        
        if not bids or len(bids) == 0:
            return 0
        
        best_bid = bids[0][0]
        
        for price, amount in bids:
            # Chỉ tính các bid trong khoảng 2% dưới best bid
            if price >= best_bid * 0.98:
                total_support += price * amount
            
            if total_support >= depth_usd:
                break
                
        return total_support
    
    def calculate_ask_resistance(self, orderbook: dict, depth_usd: float = 100000) -> float:
        """
        Tính tổng ask resistance trong khoảng depth_usd
        """
        asks = orderbook['asks']
        total_resistance = 0
        
        if not asks or len(asks) == 0:
            return 0
        
        best_ask = asks[0][0]
        
        for price, amount in asks:
            # Chỉ tính các ask trong khoảng 2% trên best ask
            if price <= best_ask * 1.02:
                total_resistance += price * amount
            
            if total_resistance >= depth_usd:
                break
                
        return total_resistance
    
    def update_orderbook_history(self, symbol: str, orderbook: dict):
        """
        Cập nhật lịch sử orderbook để tính baseline
        """
        if symbol not in self.orderbook_history:
            self.orderbook_history[symbol] = []
        
        timestamp = datetime.now()
        bid_support = self.calculate_bid_support(orderbook)
        ask_resistance = self.calculate_ask_resistance(orderbook)
        
        self.orderbook_history[symbol].append((timestamp, bid_support, ask_resistance))
        
        # Chỉ giữ lại 30 phút gần nhất
        cutoff_time = timestamp - timedelta(minutes=self.baseline_window)
        self.orderbook_history[symbol] = [
            (t, b, a) for t, b, a in self.orderbook_history[symbol]
            if t > cutoff_time
        ]
    
    def get_baseline_stats(self, symbol: str) -> Tuple[float, float, float, float]:
        """
        Tính baseline statistics từ lịch sử orderbook
        Returns: (mean_bid_support, std_bid_support, mean_bid_ask_ratio, std_bid_ask_ratio)
        """
        if symbol not in self.orderbook_history or len(self.orderbook_history[symbol]) < 10:
            return None, None, None, None
        
        history = self.orderbook_history[symbol]
        
        bid_supports = [b for _, b, _ in history]
        ask_resistances = [a for _, _, a in history]
        
        # Tính bid/ask ratios
        bid_ask_ratios = [
            b / a if a > 0 else 0
            for b, a in zip(bid_supports, ask_resistances)
        ]
        
        mean_bid_support = np.mean(bid_supports)
        std_bid_support = np.std(bid_supports)
        mean_bid_ask_ratio = np.mean(bid_ask_ratios)
        std_bid_ask_ratio = np.std(bid_ask_ratios)
        
        return mean_bid_support, std_bid_support, mean_bid_ask_ratio, std_bid_ask_ratio
    
    def detect_wall_removal(self, symbol: str, orderbook: dict) -> Dict:
        """
        Phát hiện MM rút tường đỡ giá (Support Wall Removal)
        Sử dụng statistical anomaly detection
        
        Returns: {
            'detected': bool,
            'severity': 'critical' | 'warning' | 'info',
            'current_bid_support': float,
            'baseline_bid_support': float,
            'std_deviations': float,
            'current_bid_ask_ratio': float,
            'baseline_bid_ask_ratio': float,
            'message': str
        }
        """
        # Update history
        self.update_orderbook_history(symbol, orderbook)
        
        # Get baseline stats
        mean_bid, std_bid, mean_ratio, std_ratio = self.get_baseline_stats(symbol)
        
        if mean_bid is None:
            return {
                'detected': False,
                'severity': 'info',
                'message': 'Chưa đủ dữ liệu lịch sử để phân tích'
            }
        
        # Calculate current values
        current_bid = self.calculate_bid_support(orderbook)
        current_ask = self.calculate_ask_resistance(orderbook)
        current_ratio = current_bid / current_ask if current_ask > 0 else 0
        
        # Calculate deviations
        bid_std_dev = (mean_bid - current_bid) / std_bid if std_bid > 0 else 0
        ratio_std_dev = (mean_ratio - current_ratio) / std_ratio if std_ratio > 0 else 0
        
        # Detection logic
        detected = False
        severity = 'info'
        message = ''
        
        # Critical: Bid support giảm >2 std deviations VÀ ratio giảm >1.5 std deviations
        if bid_std_dev > 2.0 and ratio_std_dev > 1.5:
            detected = True
            severity = 'critical'
            message = f'🚨 MM RÚT TƯỜNG ĐỠ GIÁ! Bid support giảm {bid_std_dev:.1f} std dev, Bid/Ask ratio giảm {ratio_std_dev:.1f} std dev'
        
        # Warning: Bid support giảm >1.5 std deviations
        elif bid_std_dev > 1.5:
            detected = True
            severity = 'warning'
            message = f'⚠️ Bid support giảm bất thường ({bid_std_dev:.1f} std dev)'
        
        # Info: Bid/Ask ratio giảm xuống <0.7
        elif current_ratio < 0.7 and mean_ratio > 1.0:
            detected = True
            severity = 'info'
            message = f'📊 Bid/Ask ratio giảm xuống {current_ratio:.2f} (từ {mean_ratio:.2f})'
        
        return {
            'detected': detected,
            'severity': severity,
            'current_bid_support': current_bid,
            'baseline_bid_support': mean_bid,
            'std_deviations': bid_std_dev,
            'current_bid_ask_ratio': current_ratio,
            'baseline_bid_ask_ratio': mean_ratio,
            'message': message
        }
    
    def detect_liquidity_drain(self, symbol: str, orderbook: dict) -> Dict:
        """
        Phát hiện thanh khoản cạn kiệt (Liquidity Withdrawal)
        
        Returns: {
            'detected': bool,
            'severity': str,
            'total_depth': float,
            'spread_pct': float,
            'message': str
        }
        """
        bids = orderbook.get('bids', [])
        asks = orderbook.get('asks', [])
        
        if not bids or not asks:
            return {'detected': False, 'severity': 'info', 'message': 'Không có dữ liệu orderbook'}
        
        # Calculate total depth (top 20 levels)
        bid_depth = sum(price * amount for price, amount in bids[:20])
        ask_depth = sum(price * amount for price, amount in asks[:20])
        total_depth = bid_depth + ask_depth
        
        # Calculate spread
        best_bid = bids[0][0]
        best_ask = asks[0][0]
        spread_pct = ((best_ask - best_bid) / best_bid) * 100
        
        detected = False
        severity = 'info'
        message = ''
        
        # Critical: Spread >1% (rất cao cho crypto)
        if spread_pct > 1.0:
            detected = True
            severity = 'critical'
            message = f'🔴 THANH KHOẢN CẠN KIỆT! Spread: {spread_pct:.2f}% (rất cao)'
        
        # Warning: Spread >0.5%
        elif spread_pct > 0.5:
            detected = True
            severity = 'warning'
            message = f'⚠️ Spread tăng cao: {spread_pct:.2f}%'
        
        # Info: Total depth thấp (<$50k)
        elif total_depth < 50000:
            detected = True
            severity = 'info'
            message = f'📊 Thanh khoản thấp: ${total_depth/1000:.1f}k'
        
        return {
            'detected': detected,
            'severity': severity,
            'total_depth': total_depth,
            'spread_pct': spread_pct,
            'message': message
        }
    
    def analyze_mm_exit_signals(self, symbol: str) -> Dict:
        """
        Phân tích tổng hợp các tín hiệu MM rút lui
        
        Returns: {
            'risk_score': int (0-100),
            'signals': List[Dict],
            'recommendation': str
        }
        """
        try:
            # Fetch orderbook
            orderbook = self.exchange.fetch_order_book(symbol, limit=100)
            
            signals = []
            risk_score = 0
            
            # Check wall removal
            wall_signal = self.detect_wall_removal(symbol, orderbook)
            if wall_signal['detected']:
                signals.append({
                    'type': 'wall_removal',
                    'severity': wall_signal['severity'],
                    'message': wall_signal['message'],
                    'data': wall_signal
                })
                
                # Add to risk score
                if wall_signal['severity'] == 'critical':
                    risk_score += 40
                elif wall_signal['severity'] == 'warning':
                    risk_score += 20
                else:
                    risk_score += 10
            
            # Check liquidity drain
            liquidity_signal = self.detect_liquidity_drain(symbol, orderbook)
            if liquidity_signal['detected']:
                signals.append({
                    'type': 'liquidity_drain',
                    'severity': liquidity_signal['severity'],
                    'message': liquidity_signal['message'],
                    'data': liquidity_signal
                })
                
                # Add to risk score
                if liquidity_signal['severity'] == 'critical':
                    risk_score += 30
                elif liquidity_signal['severity'] == 'warning':
                    risk_score += 15
                else:
                    risk_score += 5
            
            # Generate recommendation
            if risk_score >= 60:
                recommendation = '🔴 NGUY HIỂM CAO - Đóng Long ngay, cân nhắc Short'
            elif risk_score >= 40:
                recommendation = '⚠️ CẢNH BÁO - Giảm leverage, chuẩn bị thoát'
            elif risk_score >= 20:
                recommendation = '📊 THEO DÕI - Cẩn thận với vị thế Long mới'
            else:
                recommendation = '✅ BÌNH THƯỜNG - Chưa có dấu hiệu MM rút'
            
            return {
                'symbol': symbol,
                'risk_score': min(risk_score, 100),
                'signals': signals,
                'recommendation': recommendation,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"[ERROR] Failed to analyze MM exit signals for {symbol}: {e}")
            return {
                'symbol': symbol,
                'risk_score': 0,
                'signals': [],
                'recommendation': '❌ Lỗi khi phân tích',
                'error': str(e)
            }
