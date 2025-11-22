"""
Demo Script - Test Alert System (Windows Compatible)
Demonstrates the new alert system with real market data
"""

import asyncio
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from alert_orchestrator import AlertOrchestrator

async def demo_alert_system():
    """Demo the enhanced alert system"""
    
    print("="*70)
    print("CRYPTO RADAR - ENHANCED ALERT SYSTEM DEMO")
    print("="*70)
    print()
    
    # Initialize orchestrator
    orchestrator = AlertOrchestrator()
    
    # Test coins (popular volatile coins)
    test_symbols = [
        'BTC/USDT:USDT',
        'ETH/USDT:USDT',
    ]
    
    print("Testing with popular coins:")
    for symbol in test_symbols:
        print(f"   - {symbol}")
    print()
    
    # Analyze each coin
    for symbol in test_symbols:
        print("\n" + "="*70)
        print(f"ANALYZING: {symbol}")
        print("="*70)
        
        try:
            # Comprehensive analysis
            analysis = orchestrator.analyze_coin(symbol)
            
            if analysis.get('error'):
                print(f"ERROR: {analysis['error']}")
                continue
            
            # Display results
            risk_score = analysis['risk_score']
            severity = analysis['severity']
            signals = analysis['signals']
            recommendation = analysis['recommendation']
            
            # Risk score indicator
            if risk_score >= 80:
                risk_level = "[CRITICAL]"
            elif risk_score >= 60:
                risk_level = "[WARNING]"
            elif risk_score >= 40:
                risk_level = "[CAUTION]"
            else:
                risk_level = "[NORMAL]"
            
            print(f"\nRISK SCORE: {risk_score}/100 {risk_level}")
            print(f"SEVERITY: {severity.upper()}")
            print()
            
            # Display signals
            if signals:
                print("DETECTED SIGNALS:")
                for i, signal in enumerate(signals, 1):
                    print(f"\n   {i}. {signal['type'].upper()}")
                    print(f"      Severity: {signal['severity']}")
                    print(f"      Message: {signal['message']}")
                    
                    # Show additional data
                    if 'data' in signal:
                        data = signal['data']
                        if 'price_change' in data:
                            print(f"      Price Change: {data['price_change']:.2f}%")
                        if 'volume_ratio' in data:
                            print(f"      Volume Ratio: {data['volume_ratio']:.2f}x")
                        if 'std_deviations' in data:
                            print(f"      Std Deviations: {data['std_deviations']:.2f}")
            else:
                print("No significant signals detected - Market looks normal")
            
            print()
            print("RECOMMENDATION:")
            # Remove emoji from recommendation
            rec_clean = recommendation.replace('🔴', '[CRITICAL]')
            rec_clean = rec_clean.replace('⚠️', '[WARNING]')
            rec_clean = rec_clean.replace('📊', '[CAUTION]')
            rec_clean = rec_clean.replace('📈', '[WATCH]')
            rec_clean = rec_clean.replace('✅', '[OK]')
            rec_clean = rec_clean.replace('•', '-')
            print(rec_clean)
            
        except Exception as e:
            print(f"ERROR analyzing {symbol}: {e}")
            import traceback
            traceback.print_exc()
        
        # Small delay between coins
        await asyncio.sleep(2)
    
    print("\n" + "="*70)
    print("DEMO COMPLETED")
    print("="*70)
    print()
    print("Summary:")
    print("   - Analyzed multiple coins with real market data")
    print("   - Demonstrated multi-signal detection")
    print("   - Showed risk scoring (0-100)")
    print("   - Generated actionable recommendations")
    print()
    print("Next Steps:")
    print("   1. Review the alerts above")
    print("   2. Adjust thresholds if needed in implementation_plan.md")
    print("   3. Run the full bot with: python alert_bot.py")
    print()

if __name__ == "__main__":
    print("\nStarting demo... Please wait...\n")
    asyncio.run(demo_alert_system())
