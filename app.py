from flask import Flask, render_template, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import os

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

HF_API_TOKEN = os.environ.get('HF_API_TOKEN')

# Initialize HuggingFace client
client = InferenceClient(token=HF_API_TOKEN)

# Initialize components
embeddings = download_hugging_face_embeddings()
docsearch = PineconeVectorStore.from_existing_index(
    index_name="medical-chatbot",
    embedding=embeddings
)

def get_medical_answer(question):
    try:
        # Get relevant documents from Pinecone
        docs = docsearch.similarity_search(question, k=3)
        context = "\n".join([doc.page_content for doc in docs])
        
        print(f"🔍 Calling HuggingFace API...")
        
        # Use chat completion format
        messages = [
            {
                "role": "system",
                "content": "You are a helpful medical assistant. Use the provided context to answer questions accurately and always remind users to consult doctors for professional medical advice."
            },
            {
                "role": "user",
                "content": f"Medical Context:\n{context}\n\nQuestion: {question}"
            }
        ]
        
        # Call HuggingFace using chat completion
        response = client.chat_completion(
            messages=messages,
            model="mistralai/Mistral-7B-Instruct-v0.2",
            max_tokens=500,
            temperature=0.3
        )
        
        # Extract the answer
        answer = response.choices[0].message.content
        
        print(f"✅ Response received: {answer[:100]}...")
        
        return answer.strip()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return f"I apologize, but I'm having trouble processing your question. Please try again."

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    user_question = request.form["msg"]
    print(f"Question: {user_question}")
    
    answer = get_medical_answer(user_question)
    print(f"Answer: {answer}")
    
    return answer

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)