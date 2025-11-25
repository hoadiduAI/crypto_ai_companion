"""
Test script để kiểm tra Gemini API key
"""
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import google.generativeai as genai
import os

# Get API key from .env file or environment
api_key = os.getenv("GEMINI_API_KEY")

# Try to read from .env file if not in environment
if not api_key and os.path.exists(".env"):
    print("Reading API key from .env file...")
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                api_key = line.split("=", 1)[1].strip()
                print(f"Found API key: {api_key[:20]}...")
                break

if not api_key:
    print("❌ GEMINI_API_KEY chưa được set!")
    print("\nHãy chạy:")
    print('$env:GEMINI_API_KEY="your-key-here"')
    exit(1)

print(f"✅ API Key found: {api_key[:20]}...")

# Configure
genai.configure(api_key=api_key)

# List available models
print("\n📋 Đang kiểm tra models có sẵn...")
try:
    models = genai.list_models()
    print("\n✅ Models có thể dùng:")
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"  - {model.name}")
except Exception as e:
    print(f"❌ Lỗi khi list models: {e}")
    exit(1)

# Test với model đơn giản nhất
print("\n🧪 Test với model gemini-pro...")
try:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Say hello in Vietnamese")
    print(f"\n✅ SUCCESS! Response:")
    print(response.text)
except Exception as e:
    print(f"\n❌ FAILED with gemini-pro: {e}")
    
    # Try alternative
    print("\n🧪 Thử với gemini-1.5-flash...")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say hello in Vietnamese")
        print(f"\n✅ SUCCESS! Response:")
        print(response.text)
        print("\n💡 Nên dùng model: gemini-1.5-flash")
    except Exception as e2:
        print(f"\n❌ FAILED with gemini-1.5-flash: {e2}")
        
        # Try with models/ prefix
        print("\n🧪 Thử với models/gemini-1.5-flash...")
        try:
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            response = model.generate_content("Say hello in Vietnamese")
            print(f"\n✅ SUCCESS! Response:")
            print(response.text)
            print("\n💡 Nên dùng model: models/gemini-1.5-flash")
        except Exception as e3:
            print(f"\n❌ FAILED: {e3}")
            print("\n⚠️ Có vấn đề với API key hoặc project setup!")
