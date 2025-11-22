"""
Test script for user database operations
Run this to verify database functionality before testing the bot
"""

import user_db
from datetime import datetime, timedelta

def test_user_operations():
    """Test user CRUD operations"""
    print("="*60)
    print("Testing User Operations")
    print("="*60)
    
    # Test 1: Create user
    print("\n1. Creating new user...")
    user = user_db.create_user(123456789, "testuser")
    if user:
        print(f"✅ User created: {user}")
    else:
        print("⚠️ User already exists")
    
    # Test 2: Get user
    print("\n2. Getting user...")
    user = user_db.get_user(123456789)
    print(f"✅ User retrieved: {user}")
    
    # Test 3: Get status
    print("\n3. Getting user status...")
    status = user_db.get_user_status(123456789)
    print(f"✅ Status: {status}")
    
    print("\n" + "="*60)

def test_coin_tracking():
    """Test coin tracking operations"""
    print("="*60)
    print("Testing Coin Tracking")
    print("="*60)
    
    telegram_id = 123456789
    
    # Test 1: Add coin (should succeed - free tier has 1 slot)
    print("\n1. Adding BTC/USDT...")
    success = user_db.add_tracked_coin(telegram_id, "BTC/USDT")
    print(f"✅ Added: {success}")
    
    # Test 2: Try to add another coin (should fail - free tier limit)
    print("\n2. Trying to add ETH/USDT (should fail)...")
    success = user_db.add_tracked_coin(telegram_id, "ETH/USDT")
    print(f"❌ Added: {success} (expected False)")
    
    # Test 3: List tracked coins
    print("\n3. Listing tracked coins...")
    coins = user_db.get_tracked_coins(telegram_id)
    print(f"✅ Tracked coins: {coins}")
    
    # Test 4: Get users tracking BTC/USDT
    print("\n4. Finding users tracking BTC/USDT...")
    users = user_db.get_users_tracking_coin("BTC/USDT")
    print(f"✅ Users tracking BTC/USDT: {users}")
    
    # Test 5: Remove coin
    print("\n5. Removing BTC/USDT...")
    success = user_db.remove_tracked_coin(telegram_id, "BTC/USDT")
    print(f"✅ Removed: {success}")
    
    # Test 6: List again
    print("\n6. Listing tracked coins after removal...")
    coins = user_db.get_tracked_coins(telegram_id)
    print(f"✅ Tracked coins: {coins}")
    
    print("\n" + "="*60)

def test_subscription_upgrade():
    """Test subscription tier upgrades"""
    print("="*60)
    print("Testing Subscription Upgrades")
    print("="*60)
    
    telegram_id = 123456789
    
    # Test 1: Upgrade to Basic
    print("\n1. Upgrading to Basic tier...")
    expires = datetime.now() + timedelta(days=30)
    success = user_db.update_subscription(telegram_id, 'basic', expires)
    print(f"✅ Upgraded: {success}")
    
    # Test 2: Check status
    print("\n2. Checking status after upgrade...")
    status = user_db.get_user_status(telegram_id)
    print(f"✅ Status: {status}")
    
    # Test 3: Add multiple coins (should succeed now)
    print("\n3. Adding 5 coins (Basic tier limit)...")
    coins_to_add = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "XRP/USDT"]
    for coin in coins_to_add:
        success = user_db.add_tracked_coin(telegram_id, coin)
        print(f"  - {coin}: {success}")
    
    # Test 4: Try to add 6th coin (should fail)
    print("\n4. Trying to add 6th coin (should fail)...")
    success = user_db.add_tracked_coin(telegram_id, "ADA/USDT")
    print(f"❌ Added: {success} (expected False)")
    
    # Test 5: Final status
    print("\n5. Final status...")
    status = user_db.get_user_status(telegram_id)
    print(f"✅ Status: {status}")
    
    print("\n" + "="*60)

def cleanup():
    """Clean up test data"""
    print("\n" + "="*60)
    print("Cleaning up test data...")
    print("="*60)
    
    import sqlite3
    conn = sqlite3.connect(user_db.DB_PATH)
    cursor = conn.cursor()
    
    # Delete test user and their tracked coins (CASCADE will handle tracked_coins)
    cursor.execute("DELETE FROM users WHERE telegram_id = ?", (123456789,))
    conn.commit()
    conn.close()
    
    print("✅ Test data cleaned up")

if __name__ == "__main__":
    print("\nStarting Database Tests\n")
    
    try:
        test_user_operations()
        test_coin_tracking()
        test_subscription_upgrade()
        
        print("\n\n✅ All tests completed successfully!")
        print("\nYou can now:")
        print("1. Run the alert bot: python alert_bot.py")
        print("2. Test bot commands via Telegram")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Ask user if they want to clean up
        response = input("\nClean up test data? (y/n): ")
        if response.lower() == 'y':
            cleanup()
        else:
            print("Test data kept in database")
