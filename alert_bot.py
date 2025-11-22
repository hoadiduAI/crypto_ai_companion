"""
Crypto Radar Alert Bot
Enhanced version with comprehensive MM exit detection, price movement analysis, and volume surge detection
Sends personalized alerts to users tracking specific coins via Telegram
"""

import ccxt
import pandas as pd
import time
import os
from dotenv import load_dotenv
from datetime import datetime
from telegram import Bot
from telegram.ext import Application
import asyncio
import user_db
import bot_commands
import mm_detector

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Alert tracking to avoid spam
last_alerts = {}  # {symbol: timestamp}
ALERT_COOLDOWN = 3600  # 1 hour between alerts for same coin (can be overridden by orchestrator)

async def send_alert_to_user(bot: Bot, telegram_id: int, message: str):
    """Send alert message to a specific user"""
    try:
        await bot.send_message(
            chat_id=telegram_id,
            text=message,
            parse_mode='Markdown'
        )
        print(f"[OK] Alert sent to user {telegram_id}")
    except Exception as e:
        print(f"[ERROR] Failed to send alert to {telegram_id}: {e}")

async def send_alert_to_users(bot: Bot, symbol: str, message: str):
    """Send alert to all users tracking this coin"""
    users = user_db.get_users_tracking_coin(symbol)
    
    if not users:
        print(f"[INFO] No users tracking {symbol}, skipping alert")
        return
    
    print(f"[ALERT] Sending alert for {symbol} to {len(users)} user(s)")
    
    # Send to all users concurrently
    tasks = []
    for user in users:
        task = send_alert_to_user(bot, user['telegram_id'], message)
        tasks.append(task)
    
    await asyncio.gather(*tasks)

async def scan_and_alert(bot: Bot):
    """Main scanning function - Enhanced with comprehensive detection"""
    print(f"\n{'='*60}")
    print(f"[SCAN] Scanning market at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    try:
        # Import alert orchestrator
        from alert_orchestrator import AlertOrchestrator
        orchestrator = AlertOrchestrator()
        
        # Get all tracked coins from database
        # Get unique symbols from all users
        all_users = user_db.get_all_users()
        tracked_symbols = set()
        
        for user in all_users:
            coins = user_db.get_tracked_coins(user['telegram_id'])
            for coin in coins:
                tracked_symbols.add(coin['symbol'])
        
        if not tracked_symbols:
            print("[INFO] No coins being tracked by any user")
            return
        
        print(f"[INFO] Analyzing {len(tracked_symbols)} tracked coins...")
        
        # Analyze each tracked coin
        for symbol in tracked_symbols:
            try:
                print(f"\n[ANALYZING] {symbol}...")
                
                # Comprehensive analysis
                analysis = orchestrator.analyze_coin(symbol)
                
                if analysis.get('error'):
                    print(f"[ERROR] {symbol}: {analysis['error']}")
                    continue
                
                risk_score = analysis['risk_score']
                severity = analysis['severity']
                signals = analysis['signals']
                
                print(f"[RESULT] {symbol}: Risk Score = {risk_score}/100, Severity = {severity}")
                print(f"[SIGNALS] Found {len(signals)} signals")
                
                # Check if we should send alert
                last_alert = last_alerts.get(symbol, 0)
                should_alert = orchestrator.should_send_alert(
                    risk_score=risk_score,
                    severity=severity,
                    last_alert_time=last_alert if last_alert > 0 else None,
                    cooldown=ALERT_COOLDOWN
                )
                
                if not should_alert:
                    print(f"[SKIP] {symbol}: Cooldown active")
                    continue
                
                # Only send if there are actual signals
                if not signals:
                    print(f"[SKIP] {symbol}: No signals detected")
                    continue
                
                # Send alert to users tracking this coin
                users = user_db.get_users_tracking_coin(symbol)
                
                if not users:
                    print(f"[SKIP] {symbol}: No users tracking")
                    continue
                
                print(f"[ALERT] Sending alert for {symbol} to {len(users)} user(s)")
                
                # Send to all users
                alert_message = analysis['alert_message']
                await send_alert_to_users(bot, symbol, alert_message)
                
                # Update last alert time
                last_alerts[symbol] = time.time()
                
            except Exception as e:
                print(f"[ERROR] Failed to analyze {symbol}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        print(f"\n[OK] Scan completed\n")
        
    except Exception as e:
        print(f"[ERROR] Scan failed: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main bot loop"""
    if not BOT_TOKEN or "your_" in BOT_TOKEN:
        print("[ERROR] TELEGRAM_BOT_TOKEN not set in .env file")
        print("Please set your bot token in .env file:")
        print("TELEGRAM_BOT_TOKEN=your_actual_bot_token_here")
        return
    
    print("[BOT] Starting Crypto Radar Alert Bot (Enhanced Version)...")
    print(f"[TIME] Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("[FEATURES] MM Exit Detection, Price Movement Analysis, Volume Surge Detection")
    
    # Create bot application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Setup command handlers
    bot_commands.setup_bot_commands(application)
    
    # Start bot (non-blocking)
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    print("[OK] Bot is running and listening for commands")
    print("[SCANNER] Starting enhanced market scanner...")
    print(f"[CONFIG] Scan interval: 5 minutes (for tracked coins)")
    print(f"[CONFIG] Smart cooldown: Critical=0min, Warning=30min, Info=60min")
    print("\nPress Ctrl+C to stop\n")
    
    # Get bot instance for sending alerts
    bot = application.bot
    
    try:
        while True:
            await scan_and_alert(bot)
            
            # Wait 5 minutes before next scan (more frequent for better detection)
            print(f"[WAIT] Next scan in 5 minutes...")
            await asyncio.sleep(300)  # 5 minutes
            
    except KeyboardInterrupt:
        print("\n\n[STOP] Stopping bot...")
        await application.stop()
        await application.shutdown()
        print("[OK] Bot stopped successfully")

if __name__ == "__main__":
    asyncio.run(main())
