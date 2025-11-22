"""
User Database Module for Crypto Radar
Manages users, subscriptions, and tracked coins using SQLite
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import os
import random
import string

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'users.db')

# Subscription tier limits
TIER_LIMITS = {
    'free': 1,
    'basic': 5,
    'pro': float('inf')
}

def init_db():
    """Initialize database with required tables"""
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            username TEXT,
            subscription_tier TEXT DEFAULT 'free',
            subscription_expires DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tracked coins table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracked_coins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (telegram_id) REFERENCES users(telegram_id) ON DELETE CASCADE,
            UNIQUE(telegram_id, symbol)
        )
    ''')
    
    # Auth codes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS auth_codes (
            code TEXT PRIMARY KEY,
            telegram_id INTEGER NOT NULL,
            expires_at DATETIME NOT NULL,
            FOREIGN KEY (telegram_id) REFERENCES users(telegram_id) ON DELETE CASCADE
        )
    ''')
    
    # Create indexes for better query performance
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_tracked_coins_telegram_id 
        ON tracked_coins(telegram_id)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_tracked_coins_symbol 
        ON tracked_coins(symbol)
    ''')
    
    conn.commit()
    conn.close()

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

# ==================== AUTH OPERATIONS ====================

def create_login_code(telegram_id: int) -> str:
    """Generate a 6-digit login code valid for 5 minutes"""
    code = ''.join(random.choices(string.digits, k=6))
    expires_at = datetime.now() + timedelta(minutes=5)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Clean up old codes for this user
    cursor.execute('DELETE FROM auth_codes WHERE telegram_id = ?', (telegram_id,))
    
    # Insert new code
    cursor.execute('''
        INSERT INTO auth_codes (code, telegram_id, expires_at)
        VALUES (?, ?, ?)
    ''', (code, telegram_id, expires_at))
    
    conn.commit()
    conn.close()
    
    return code

def verify_login_code(code: str) -> Optional[int]:
    """
    Verify login code. Returns telegram_id if valid, None otherwise.
    Deletes code after successful verification.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT telegram_id, expires_at FROM auth_codes WHERE code = ?', (code,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return None
    
    telegram_id = row['telegram_id']
    expires_at = datetime.fromisoformat(row['expires_at'])
    
    if datetime.now() > expires_at:
        # Expired
        cursor.execute('DELETE FROM auth_codes WHERE code = ?', (code,))
        conn.commit()
        conn.close()
        return None
    
    # Valid - Delete code to prevent reuse
    cursor.execute('DELETE FROM auth_codes WHERE telegram_id = ?', (telegram_id,))
    conn.commit()
    conn.close()
    
    return telegram_id

# ==================== USER OPERATIONS ====================

def create_user(telegram_id: int, username: str = None) -> Dict:
    """
    Create a new user with free tier
    Returns user data or None if user already exists
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO users (telegram_id, username, subscription_tier)
            VALUES (?, ?, 'free')
        ''', (telegram_id, username))
        conn.commit()
        
        return get_user(telegram_id)
    except sqlite3.IntegrityError:
        # User already exists
        return None
    finally:
        conn.close()

def get_user(telegram_id: int) -> Optional[Dict]:
    """Get user by telegram_id"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None

def update_subscription(telegram_id: int, tier: str, expires_at: datetime = None) -> bool:
    """
    Update user's subscription tier
    tier: 'free', 'basic', or 'pro'
    expires_at: expiration date for paid tiers
    """
    if tier not in TIER_LIMITS:
        raise ValueError(f"Invalid tier: {tier}. Must be one of {list(TIER_LIMITS.keys())}")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users 
        SET subscription_tier = ?, 
            subscription_expires = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE telegram_id = ?
    ''', (tier, expires_at, telegram_id))
    
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    
    return success

def check_subscription_expired(telegram_id: int) -> bool:
    """
    Check if user's subscription has expired
    If expired, downgrade to free tier
    Returns True if expired and downgraded
    """
    user = get_user(telegram_id)
    if not user:
        return False
    
    if user['subscription_tier'] == 'free':
        return False
    
    if user['subscription_expires']:
        expires = datetime.fromisoformat(user['subscription_expires'])
        if datetime.now() > expires:
            # Downgrade to free
            update_subscription(telegram_id, 'free')
            return True
    
    return False

# ==================== TRACKED COINS OPERATIONS ====================

def can_add_coin(telegram_id: int) -> bool:
    """Check if user can add more coins based on their tier"""
    user = get_user(telegram_id)
    if not user:
        return False
    
    # Check if subscription expired
    check_subscription_expired(telegram_id)
    user = get_user(telegram_id)  # Refresh user data
    
    tier = user['subscription_tier']
    limit = TIER_LIMITS.get(tier, 0)
    
    current_count = get_tracked_coins_count(telegram_id)
    return current_count < limit

def get_tracked_coins_count(telegram_id: int) -> int:
    """Get number of coins user is tracking"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(*) as count 
        FROM tracked_coins 
        WHERE telegram_id = ?
    ''', (telegram_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    return result['count'] if result else 0

def add_tracked_coin(telegram_id: int, symbol: str) -> bool:
    """
    Add a coin to user's tracking list
    Returns True if successful, False if limit reached or already tracking
    """
    if not can_add_coin(telegram_id):
        return False
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO tracked_coins (telegram_id, symbol)
            VALUES (?, ?)
        ''', (telegram_id, symbol))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Already tracking this coin
        return False
    finally:
        conn.close()

def remove_tracked_coin(telegram_id: int, symbol: str) -> bool:
    """Remove a coin from user's tracking list"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM tracked_coins 
        WHERE telegram_id = ? AND symbol = ?
    ''', (telegram_id, symbol))
    
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    
    return success

def get_tracked_coins(telegram_id: int) -> List[Dict]:
    """Get all coins tracked by a user"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT symbol, added_at 
        FROM tracked_coins 
        WHERE telegram_id = ?
        ORDER BY added_at DESC
    ''', (telegram_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def get_users_tracking_coin(symbol: str) -> List[Dict]:
    """
    Get all users tracking a specific coin
    Returns list of user dictionaries
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT u.telegram_id, u.username, u.subscription_tier
        FROM users u
        INNER JOIN tracked_coins tc ON u.telegram_id = tc.telegram_id
        WHERE tc.symbol = ?
    ''', (symbol,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def get_user_status(telegram_id: int) -> Dict:
    """
    Get user's subscription status including coins tracked and slots available
    """
    user = get_user(telegram_id)
    if not user:
        return None
    
    # Check expiration
    check_subscription_expired(telegram_id)
    user = get_user(telegram_id)  # Refresh
    
    tier = user['subscription_tier']
    limit = TIER_LIMITS.get(tier, 0)
    tracked_count = get_tracked_coins_count(telegram_id)
    
    return {
        'telegram_id': user['telegram_id'],
        'username': user['username'],
        'tier': tier,
        'tracked_count': tracked_count,
        'limit': limit,
        'slots_available': limit - tracked_count,
        'subscription_expires': user['subscription_expires']
    }

# Initialize database on module import
init_db()
