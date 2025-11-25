import requests
import sys
import json

# Set encoding for stdout to utf-8 to handle Vietnamese characters
sys.stdout.reconfigure(encoding='utf-8')

try:
    # Test API
    print("Sending request to http://localhost:8000/analyze...")
    response = requests.post(
        "http://localhost:8000/analyze",
        data={"text": "Phân tích BTC hiện tại"}
    )

    print("Status:", response.status_code)
    print("\nResponse:")
    # Pretty print the JSON
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
except Exception as e:
    print(f"Error: {e}")
    print("Make sure the backend is running: python ai_chat_api.py")
