"""
Crypto Radar Alert Bot
Scans Binance Futures for Ghost Towns and Fake Pumps
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
ALERT_COOLDOWN = 3600  # 1 hour between alerts for same coin

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

def should_send_alert(symbol: str) -> bool:
    """Check if we should send alert for this coin (cooldown check)"""
    now = time.time()
    
    if symbol in last_alerts:
        time_since_last = now - last_alerts[symbol]
        if time_since_last < ALERT_COOLDOWN:
            return False
    
    last_alerts[symbol] = now
    return True

async def scan_and_alert(bot: Bot):
    """Main scanning function - runs periodically"""
    print(f"\n{'='*60}")
    print(f"[SCAN] Scanning market at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    # Fetch data
    df = mm_detector.fetch_binance_data()
    
    if df.empty:
        print("[WARNING] No data fetched, skipping this cycle")
        return
    
    print(f"[DATA] Fetched {len(df)} coins from Binance Futures")
    
    # Detect anomalies
    ghost_towns = mm_detector.detect_ghost_towns(df)
    fake_pumps = mm_detector.detect_fake_pumps(df)
    
    print(f"[GHOST] Found {len(ghost_towns)} Ghost Towns")
    print(f"[PUMP] Found {len(fake_pumps)} Fake Pumps")
    
    # Send alerts for Ghost Towns
    for _, coin in ghost_towns.iterrows():
        symbol = coin['Symbol']
        
        # Check cooldown
        if not should_send_alert(symbol):
            continue
        
        # Check if anyone is tracking this coin
        users = user_db.get_users_tracking_coin(symbol)
        if not users:
            continue
        
        message = f"""
🚨 **GHOST TOWN ALERT**

**Coin:** {symbol}
**Giá:** ${coin['Price']:.4f}
**Volume 24h:** ${coin['Volume']/1_000_000:.2f}M
**Thay đổi:** {coin['Change']:+.2f}%

⚠️ **Cảnh báo:** Giá cao nhưng volume thấp bất thường!
MM có thể đang giữ giá nhân tạo.

💡 **Khuyến nghị:**
• Kiểm tra heatmap thanh lý
• Cẩn thận với vị thế Long
• Chờ volume tăng trước khi vào lệnh

🔗 [Xem chi tiết trên Crypto Radar](http://localhost:8501)
        """
        
        await send_alert_to_users(bot, symbol, message)
    
    # Send alerts for Fake Pumps
    for _, coin in fake_pumps.iterrows():
        symbol = coin['Symbol']
        
        # Check cooldown
        if not should_send_alert(symbol):
            continue
        
        # Check if anyone is tracking this coin
        users = user_db.get_users_tracking_coin(symbol)
        if not users:
            continue
        
        message = f"""
🚀 **FAKE PUMP ALERT**

**Coin:** {symbol}
**Giá:** ${coin['Price']:.4f}
**Volume 24h:** ${coin['Volume']/1_000_000:.2f}M
**Thay đổi:** {coin['Change']:+.2f}%

⚠️ **Cảnh báo:** Tăng giá mạnh nhưng volume thấp!
Có thể là bẫy bull trap.

💡 **Khuyến nghị:**
• Không FOMO vào lệnh Long
• Chờ xác nhận với volume cao
• Cân nhắc Short nếu giá reject

🔗 [Xem chi tiết trên Crypto Radar](http://localhost:8501)
        """
        
        await send_alert_to_users(bot, symbol, message)
    
    print(f"[OK] Scan completed\n")

async def main():
    """Main bot loop"""
    if not BOT_TOKEN or "your_" in BOT_TOKEN:
        print("[ERROR] TELEGRAM_BOT_TOKEN not set in .env file")
        print("Please set your bot token in .env file:")
        print("TELEGRAM_BOT_TOKEN=your_actual_bot_token_here")
        return
    
    print("[BOT] Starting Crypto Radar Alert Bot...")
    print(f"[TIME] Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create bot application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Setup command handlers
    bot_commands.setup_bot_commands(application)
    
    # Start bot (non-blocking)
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    print("[OK] Bot is running and listening for commands")
    print("[SCANNER] Starting market scanner...")
    print(f"[CONFIG] Scan interval: 15 minutes")
    print(f"[CONFIG] Alert cooldown: {ALERT_COOLDOWN/3600:.1f} hours")
    print("\nPress Ctrl+C to stop\n")
    
    # Get bot instance for sending alerts
    bot = application.bot
    
    try:
        while True:
            await scan_and_alert(bot)
            
            # Wait 15 minutes before next scan
            print(f"[WAIT] Next scan in 15 minutes...")
            await asyncio.sleep(900)  # 15 minutes
            
    except KeyboardInterrupt:
        print("\n\n[STOP] Stopping bot...")
        await application.stop()
        await application.shutdown()
        print("[OK] Bot stopped successfully")

if __name__ == "__main__":
    asyncio.run(main())
