"""
Groq API Test Script (for groq==0.4.2)
"""

from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

print("=" * 60)
print("🧪 GROQ API TEST")
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

print("📡 Testing Groq API...")
print("Question: 'What is 2+2?'")
print()

try:
    from groq import Groq
    
    # Initialize client (v0.4.2 way)
    client = Groq(
        api_key=GROQ_API_KEY
    )
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "What is 2+2? Answer in one sentence."
            }
        ],
        model="llama-3.1-70b-versatile",
        temperature=0.7,
        max_tokens=50,
    )
    
    answer = chat_completion.choices[0].message.content
    
    print("✅ SUCCESS!")
    print(f"📝 Answer: {answer}")
    print()
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Error type: {type(e).__name__}")
    print()
    
    error_str = str(e).lower()
    
    if "api key" in error_str or "401" in error_str or "unauthorized" in error_str:
        print("🔧 SOLUTION: Invalid API key")
        print("1. Check your API key at: https://console.groq.com/keys")
        print("2. Make sure it starts with 'gsk_'")
        print("3. Update .env file")
    elif "model" in error_str:
        print("🔧 SOLUTION: Try different model")
        print("Available models: llama-3.1-70b-versatile, mixtral-8x7b-32768")
    else:
        import traceback
        traceback.print_exc()
    
    exit(1)

# Test 2: Medical question
print("📡 Testing medical question...")
print("Question: 'What is diabetes?'")
print()

try:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful medical assistant."
            },
            {
                "role": "user",
                "content": "What is diabetes? Explain briefly in 2 sentences."
            }
        ],
        model="llama-3.1-70b-versatile",
        temperature=0.3,
        max_tokens=100,
    )
    
    answer = chat_completion.choices[0].message.content
    
    print("✅ Medical question test successful!")
    print(f"📝 Answer: {answer}")
    print()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("=" * 60)
print("🎉 ALL TESTS PASSED!")
print("=" * 60)
print()
print("✅ Groq API is working!")
print("✅ You can now run: python app_render.py")
print()