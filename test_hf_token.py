"""
HuggingFace API Token Test Script
This script tests if your HuggingFace token is working correctly
"""

from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import os

# Load environment variables
load_dotenv()

HF_API_TOKEN = os.environ.get('HF_API_TOKEN')

print("=" * 60)
print("🧪 HUGGINGFACE TOKEN TEST")
print("=" * 60)

# Check if token exists
if not HF_API_TOKEN:
    print("❌ ERROR: HF_API_TOKEN not found in .env file")
    print("\nPlease add this to your .env file:")
    print('HF_API_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxx"')
    print("\nGet your token from: https://huggingface.co/settings/tokens")
    exit(1)

print(f"✅ Token found: {HF_API_TOKEN[:10]}...{HF_API_TOKEN[-5:]}")
print()

# Test 1: Initialize client
print("📡 Test 1: Initializing HuggingFace client...")
try:
    client = InferenceClient(token=HF_API_TOKEN)
    print("✅ Client initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize client: {e}")
    exit(1)

print()

# Test 2: Simple chat completion
print("📡 Test 2: Testing chat completion...")
print("Prompt: 'Hello, how are you?'")
print()

try:
    messages = [
        {"role": "user", "content": "Hello, how are you?"}
    ]
    
    response = client.chat_completion(
        messages=messages,
        model="mistralai/Mistral-7B-Instruct-v0.2",
        max_tokens=50,
        temperature=0.7
    )
    
    answer = response.choices[0].message.content
    
    print("✅ API call successful!")
    print(f"📝 Response: {answer}")
    print()
    
except Exception as e:
    print(f"❌ API call failed!")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    print()
    
    # Provide specific troubleshooting
    error_str = str(e).lower()
    
    if "unauthorized" in error_str or "401" in error_str:
        print("🔧 SOLUTION: Your token is invalid or expired")
        print("   → Go to: https://huggingface.co/settings/tokens")
        print("   → Create a new token")
        print("   → Update your .env file")
    
    elif "model" in error_str and "loading" in error_str:
        print("🔧 SOLUTION: Model is loading (cold start)")
        print("   → Wait 20-30 seconds and run this script again")
    
    elif "rate limit" in error_str or "429" in error_str:
        print("🔧 SOLUTION: Rate limit exceeded")
        print("   → Free tier: 1000 requests/day")
        print("   → Wait and try again later")
    
    elif "gated" in error_str or "access" in error_str:
        print("🔧 SOLUTION: Model requires access approval")
        print("   → Go to: https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2")
        print("   → Click 'Access repository' if prompted")
    
    else:
        print("🔧 TROUBLESHOOTING:")
        print("   → Check your internet connection")
        print("   → Verify token format: should start with 'hf_'")
        print("   → Try regenerating your token")
    
    exit(1)

# Test 3: Medical question test
print("📡 Test 3: Testing medical question...")
print("Question: 'What is diabetes?'")
print()

try:
    medical_prompt = """You are a helpful medical assistant.

Question: What is diabetes?

Answer:"""
    
    response = client.text_generation(
        medical_prompt,
        model="mistralai/Mistral-7B-Instruct-v0.2",
        max_new_tokens=100,
        temperature=0.3,
        return_full_text=False
    )
    
    print("✅ Medical question test successful!")
    print(f"📝 Response: {response}")
    print()
    
except Exception as e:
    print(f"❌ Medical question test failed: {e}")
    print()

print("=" * 60)
print("🎉 ALL TESTS COMPLETED!")
print("=" * 60)
print()
print("If all tests passed, your setup is ready for deployment!")
print("If any test failed, follow the troubleshooting steps above.")
print()