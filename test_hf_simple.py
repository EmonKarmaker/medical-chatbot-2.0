"""
Groq API Test Script (Direct REST API - No SDK)
"""

from dotenv import load_dotenv
import requests
import os

load_dotenv()

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

print("=" * 60)
print("🧪 GROQ API TEST (Direct REST)")
print("=" * 60)

if not GROQ_API_KEY:
    print("❌ GROQ_API_KEY not found in .env")
    print("\n🔧 SOLUTION:")
    print("1. Go to: https://console.groq.com/keys")
    print("2. Create API Key")
    print("3. Add to .env: GROQ_API_KEY='gsk_xxxxx'")
    exit(1)

print(f"✅ API Key found: {GROQ_API_KEY[:10]}...{GROQ_API_KEY[-5:]}")
print()

print("📡 Test 1: Simple question")
print("Question: 'What is 2+2?'")
print()

try:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": "What is 2+2? Answer in one sentence."
            }
        ],
        "temperature": 0.7,
        "max_tokens": 50
    }
    
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        answer = result['choices'][0]['message']['content']
        
        print("✅ SUCCESS!")
        print(f"📝 Answer: {answer}")
        print()
    elif response.status_code == 401:
        print("❌ Authentication Error!")
        print("🔧 SOLUTION:")
        print("1. Check your API key at: https://console.groq.com/keys")
        print("2. Make sure it starts with 'gsk_'")
        print("3. Create a new key if needed")
        exit(1)
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        exit(1)
    
except requests.exceptions.Timeout:
    print("❌ Request timed out")
    print("🔧 Check your internet connection")
    exit(1)
except requests.exceptions.ConnectionError:
    print("❌ Connection error")
    print("🔧 Check your internet connection")
    exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 2: Medical question
print("📡 Test 2: Medical question")
print("Question: 'What is diabetes?'")
print()

try:
    payload = {
        "model": "llama-3.1-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful medical assistant."
            },
            {
                "role": "user",
                "content": "What is diabetes? Explain briefly in 2 sentences."
            }
        ],
        "temperature": 0.3,
        "max_tokens": 100
    }
    
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        answer = result['choices'][0]['message']['content']
        
        print("✅ Medical question test successful!")
        print(f"📝 Answer: {answer}")
        print()
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        exit(1)
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

print("=" * 60)
print("🎉 ALL TESTS PASSED!")
print("=" * 60)
print()
print("✅ Groq API is working!")
print("✅ You can now run: python app_render.py")
print()