from flask import Flask, render_template, request
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import requests
import os

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# Global variables (will be initialized on first request)
embeddings = None
docsearch = None

def initialize_components():
    """Initialize embeddings and Pinecone on first request (lazy loading)"""
    global embeddings, docsearch
    
    if embeddings is None:
        print("🔄 Initializing embeddings (first request)...")
        from src.helper import download_hugging_face_embeddings
        embeddings = download_hugging_face_embeddings()
        
    if docsearch is None:
        print("🔄 Connecting to Pinecone...")
        docsearch = PineconeVectorStore.from_existing_index(
            index_name="medical-chatbot",
            embedding=embeddings
        )
        print("✅ Components initialized!")
    
    return docsearch

def get_medical_answer(question):
    """
    Uses Groq API via direct REST calls (no SDK needed)
    Works with any httpx version
    """
    try:
        # Initialize components on first request (lazy loading)
        docsearch = initialize_components()
        
        # Get relevant documents from Pinecone
        docs = docsearch.similarity_search(question, k=3)
        context = "\n".join([doc.page_content for doc in docs])
        
        print(f"Question: {question}")
        print(f"⚡ Using Groq API (Direct REST)...")
        
        # Prepare request
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful medical assistant. Use the provided medical context to answer questions accurately. Always remind users to consult healthcare professionals for medical advice."
                },
                {
                    "role": "user",
                    "content": f"Medical Context:\n{context}\n\nQuestion: {question}"
                }
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }
        
        # Make direct API call
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content']
            print(f"✅ Response received")
            return answer.strip()
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return "I apologize, but I'm having trouble processing your question. Please try again."
        
    except requests.exceptions.Timeout:
        print(f"⏱️ Request timeout")
        return "Request timed out. Please try again."
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return "I apologize, but I'm having trouble processing your question. Please try again."

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/health")
def health():
    """Health check endpoint for Render"""
    return {"status": "ok"}, 200

@app.route("/get", methods=["POST"])
def chat():
    user_question = request.form["msg"]
    answer = get_medical_answer(user_question)
    print(f"Answer: {answer[:200]}...")
    return answer

if __name__ == '__main__':
    print("=" * 60)
    print("⚡ USING GROQ API (Direct REST - No SDK)")
    print("=" * 60)
    
    # Get port from environment variable (Render provides this)
    port = int(os.environ.get('PORT', 8080))
    
    app.run(host="0.0.0.0", port=port, debug=False)