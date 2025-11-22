"""
Alert Orchestrator - Tích hợp tất cả detectors và tính Risk Score
Combines MM exit signals, price movements, volume analysis into comprehensive alerts
"""

import ccxt
from datetime import datetime
from typing import Dict, List
import mm_detector
import mm_exit_detector
import volume_analyzer

class AlertOrchestrator:
    def __init__(self):
        self.exchange = ccxt.binance({
            'options': {'defaultType': 'future'},
            'enableRateLimit': True
        })
        self.mm_exit_detector = mm_exit_detector.MMExitDetector(self.exchange)
    
    def calculate_risk_score(self, signals: List[Dict]) -> int:
        """
        Tính Risk Score từ 0-100 dựa trên các tín hiệu
        
        Scoring logic:
        - MM Exit Critical: +40
        - MM Exit Warning: +20
        - Price Drop Critical (>15%): +30
        - Price Drop Warning (10-15%): +15
        - Volume Surge + Sell Pressure: +20
        - Liquidity Drain Critical: +30
        """
        risk_score = 0
        
        for signal in signals:
            signal_type = signal.get('type', '')
            severity = signal.get('severity', 'info')
            
            # MM Exit signals
            if signal_type == 'wall_removal':
                if severity == 'critical':
                    risk_score += 40
                elif severity == 'warning':
                    risk_score += 20
                else:
                    risk_score += 10
            
            elif signal_type == 'liquidity_drain':
                if severity == 'critical':
                    risk_score += 30
                elif severity == 'warning':
                    risk_score += 15
                else:
                    risk_score += 5
            
            # Price movement signals
            elif signal_type == 'price_drop':
                if severity == 'critical':
                    risk_score += 30
                elif severity == 'warning':
                    risk_score += 15
            
            # Volume signals
            elif signal_type == 'volume_surge':
                if severity == 'critical':
                    risk_score += 15
                elif severity == 'warning':
                    risk_score += 10
            
            # Sell pressure
            elif signal_type == 'sell_pressure':
                if severity == 'critical':
                    risk_score += 20
                elif severity == 'warning':
                    risk_score += 10
        
        return min(risk_score, 100)
    
    def generate_recommendation(self, risk_score: int, signals: List[Dict]) -> str:
        """
        Tạo khuyến nghị hành động dựa trên risk score
        """
        if risk_score >= 80:
            return """🔴 NGUY HIỂM CỰC CAO
• ĐÓNG LONG positions ngay lập tức
• Cân nhắc mở SHORT với SL chặt
• KHÔNG mở Long mới cho đến khi ổn định"""
        
        elif risk_score >= 60:
            return """⚠️ CẢNH BÁO CAO
• Giảm leverage xuống tối thiểu
• Chuẩn bị thoát Long positions
• Đặt Stop Loss chặt
• Theo dõi sát thị trường"""
        
        elif risk_score >= 40:
            return """📊 CẢNH BÁO TRUNG BÌNH
• Cẩn thận với vị thế Long mới
• Giảm size positions
• Theo dõi volume và price action
• Chờ xác nhận trước khi vào lệnh"""
        
        elif risk_score >= 20:
            return """📈 THEO DÕI
• Có dấu hiệu bất thường nhẹ
• Tiếp tục theo dõi
• Cẩn thận khi tăng leverage"""
        
        else:
            return """✅ BÌNH THƯỜNG
• Chưa có dấu hiệu MM rút
• Có thể giao dịch bình thường
• Vẫn nên quản lý risk tốt"""
    
    def analyze_coin(self, symbol: str) -> Dict:
        """
        Phân tích toàn diện một coin
        
        Returns:
            {
                'symbol': str,
                'risk_score': int,
                'severity': 'critical' | 'warning' | 'info',
                'signals': List[Dict],
                'recommendation': str,
                'alert_message': str
            }
        """
        signals = []
        
        try:
            # 1. Check MM Exit Signals
            mm_exit_analysis = self.mm_exit_detector.analyze_mm_exit_signals(symbol)
            if mm_exit_analysis.get('signals'):
                signals.extend(mm_exit_analysis['signals'])
            
            # 2. Check Sharp Price Drop
            price_drop = mm_detector.detect_sharp_price_drop(symbol, threshold=10)
            if price_drop.get('detected'):
                signals.append({
                    'type': 'price_drop',
                    'severity': price_drop['severity'],
                    'message': price_drop['message'],
                    'data': price_drop
                })
            
            # 3. Check Sharp Price Pump (fake pump warning)
            price_pump = mm_detector.detect_sharp_price_pump(symbol, threshold=15)
            if price_pump.get('detected') and not price_pump.get('is_real_pump'):
                signals.append({
                    'type': 'fake_pump',
                    'severity': price_pump['severity'],
                    'message': price_pump['message'],
                    'data': price_pump
                })
            
            # 4. Check Volume Surge
            volume_surge = mm_detector.detect_volume_surge(symbol, threshold=2.0)
            if volume_surge.get('detected'):
                signals.append({
                    'type': 'volume_surge',
                    'severity': volume_surge['severity'],
                    'message': volume_surge['message'],
                    'data': volume_surge
                })
            
            # 5. Check Buy/Sell Pressure
            pressure = volume_analyzer.calculate_buy_sell_pressure(symbol)
            if pressure.get('sell_pressure_pct', 0) > 60:
                signals.append({
                    'type': 'sell_pressure',
                    'severity': pressure.get('severity', 'info'),
                    'message': pressure['message'],
                    'data': pressure
                })
            
            # Calculate risk score
            risk_score = self.calculate_risk_score(signals)
            
            # Determine overall severity
            if risk_score >= 80:
                severity = 'critical'
            elif risk_score >= 50:
                severity = 'warning'
            else:
                severity = 'info'
            
            # Generate recommendation
            recommendation = self.generate_recommendation(risk_score, signals)
            
            # Generate alert message
            alert_message = self.format_alert_message(symbol, risk_score, severity, signals, recommendation)
            
            return {
                'symbol': symbol,
                'risk_score': risk_score,
                'severity': severity,
                'signals': signals,
                'recommendation': recommendation,
                'alert_message': alert_message,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"[ERROR] Failed to analyze {symbol}: {e}")
            return {
                'symbol': symbol,
                'risk_score': 0,
                'severity': 'info',
                'signals': [],
                'recommendation': '❌ Lỗi khi phân tích',
                'error': str(e)
            }
    
    def format_alert_message(self, symbol: str, risk_score: int, severity: str, signals: List[Dict], recommendation: str) -> str:
        """
        Format alert message cho Telegram
        """
        # Emoji based on severity
        if severity == 'critical':
            emoji = '🚨'
            level = 'CRITICAL ALERT'
        elif severity == 'warning':
            emoji = '⚠️'
            level = 'WARNING'
        else:
            emoji = '📊'
            level = 'INFO'
        
        # Build message
        message = f"{emoji} **{level} - {symbol}**\n\n"
        message += f"**Risk Score:** {risk_score}/100\n\n"
        
        # Add signals
        if signals:
            message += "**🔍 Tín Hiệu Phát Hiện:**\n"
            for signal in signals:
                message += f"• {signal['message']}\n"
            message += "\n"
        
        # Add recommendation
        message += f"**💡 KHUYẾN NGHỊ:**\n{recommendation}\n\n"
        
        # Add timestamp
        message += f"⏰ {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}"
        
        return message
    
    def should_send_alert(self, risk_score: int, severity: str, last_alert_time: float = None, cooldown: int = 3600) -> bool:
        """
        Quyết định có nên gửi alert không dựa trên risk score và cooldown
        
        Args:
            risk_score: Risk score 0-100
            severity: 'critical' | 'warning' | 'info'
            last_alert_time: Timestamp of last alert
            cooldown: Cooldown in seconds
        
        Returns:
            bool: True if should send alert
        """
        import time
        
        # Critical alerts: Always send (no cooldown)
        if severity == 'critical' or risk_score >= 80:
            return True
        
        # Warning alerts: 30 minute cooldown
        if severity == 'warning' or risk_score >= 50:
            if last_alert_time is None:
                return True
            time_since_last = time.time() - last_alert_time
            return time_since_last >= 1800  # 30 minutes
        
        # Info alerts: 1 hour cooldown
        if last_alert_time is None:
            return True
        time_since_last = time.time() - last_alert_time
        return time_since_last >= cooldown
