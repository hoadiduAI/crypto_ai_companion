
import asyncio
import pandas as pd
from alert_bot import fetch_binance_data, detect_ghost_towns, detect_fake_pumps

def verify_scanner():
    print("1. Fetching data from Binance...")
    df = fetch_binance_data()
    
    if df.empty:
        print("[FAIL] Failed to fetch data")
        return

    print(f"[OK] Fetched {len(df)} coins")
    print(f"   Columns: {df.columns.tolist()}")
    
    print("\n2. Detecting Ghost Towns...")
    ghost_towns = detect_ghost_towns(df)
    print(f"   Found {len(ghost_towns)} Ghost Towns")
    if not ghost_towns.empty:
        print(ghost_towns.head(3).to_string())

    print("\n3. Detecting Fake Pumps...")
    fake_pumps = detect_fake_pumps(df)
    print(f"   Found {len(fake_pumps)} Fake Pumps")
    if not fake_pumps.empty:
        print(fake_pumps.head(3).to_string())

if __name__ == "__main__":
    verify_scanner()
