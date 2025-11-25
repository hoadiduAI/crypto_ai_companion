"""
Simple test client for AI Chat API
Run this to test the backend without the full HTML interface
"""

import requests
import json

API_URL = "http://localhost:8000"

def test_health():
    """Test if API is running"""
    try:
        response = requests.get(f"{API_URL}/health")
        print("✅ API Health Check:")
        print(json.dumps(response.json(), indent=2))
        return True
    except Exception as e:
        print(f"❌ API not running: {e}")
        print("\nPlease start the backend first:")
        print("  python ai_chat_api.py")
        return False

def test_analysis(query):
    """Test crypto analysis"""
    print(f"\n🔍 Testing query: '{query}'")
    print("-" * 60)
    
    try:
        response = requests.post(
            f"{API_URL}/analyze",
            data={"text": query}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Success!")
            print(f"\nSymbol detected: {result.get('symbol', 'N/A')}")
            
            if result.get('market_data'):
                print(f"\n📊 Market Data:")
                data = result['market_data']
                print(f"  Price: ${data.get('price', 0):,.2f}")
                print(f"  Change 24h: {data.get('change_24h', 0):+.2f}%")
                print(f"  Volume: ${data.get('quote_volume', 0):,.0f}")
                if 'funding_rate' in data:
                    print(f"  Funding Rate: {data['funding_rate']:.4f}%")
            
            print(f"\n🤖 AI Analysis:")
            print("-" * 60)
            print(result.get('analysis', 'No analysis'))
            print("-" * 60)
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("=" * 60)
    print("🔮 Crypto AI Chat - API Test Client")
    print("=" * 60)
    
    # Check if API is running
    if not test_health():
        return
    
    print("\n" + "=" * 60)
    print("Testing Analysis Queries")
    print("=" * 60)
    
    # Test queries
    test_queries = [
        "Phân tích BTC hiện tại",
        "ETH có đáng mua không?",
        "SOL trend như thế nào?"
    ]
    
    for query in test_queries:
        test_analysis(query)
        print("\n")

if __name__ == "__main__":
    main()
