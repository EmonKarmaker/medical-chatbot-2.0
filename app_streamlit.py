import streamlit as st
from dotenv import load_dotenv
import requests
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Medical Chatbot - AI Healthcare Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# Initialize session state
if 'embeddings' not in st.session_state:
    st.session_state.embeddings = None
if 'docsearch' not in st.session_state:
    st.session_state.docsearch = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'initialized' not in st.session_state:
    st.session_state.initialized = False

@st.cache_resource
def initialize_components():
    """Initialize embeddings and Pinecone (cached)"""
    with st.spinner("📄 Loading AI components... (This may take 20-30 seconds on first run)"):
        from src.helper import download_hugging_face_embeddings
        import pinecone
        
        # Initialize Pinecone with OLD API (pinecone-client 2.2.4)
        pinecone.init(
            api_key=PINECONE_API_KEY,
            environment="gcp-starter"
        )
        
        embeddings = download_hugging_face_embeddings()
        
        # Use OLD Pinecone API with langchain_community
        from langchain_community.vectorstores import Pinecone as LangchainPinecone
        docsearch = LangchainPinecone.from_existing_index(
            index_name="medical-chatbot",
            embedding=embeddings
        )
        
    return embeddings, docsearch

def get_medical_answer(question, docsearch):
    """Get answer using Groq API"""
    try:
        # Get relevant documents
        docs = docsearch.similarity_search(question, k=3)
        context = "\n".join([doc.page_content for doc in docs])
        
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
                    "content": "You are a helpful medical assistant. Use the provided medical context to answer questions accurately. Always remind users to consult healthcare professionals for medical advice. Keep responses concise and well-structured."
                },
                {
                    "role": "user",
                    "content": f"Medical Context:\n{context}\n\nQuestion: {question}"
                }
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }
        
        # Make API call
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content']
            return answer.strip(), context
        else:
            return "I apologize, but I'm having trouble processing your question. Please try again.", ""
        
    except Exception as e:
        return f"Error: {str(e)}", ""

# Custom CSS for bigger, better interface
st.markdown("""
    <style>
    /* Main container */
    .main {
        padding: 2rem;
    }
    
    /* Header styling */
    .big-title {
        font-size: 3.5rem !important;
        font-weight: 800;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        font-size: 1.5rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Chat messages */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        font-size: 1.2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .bot-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        font-size: 1.1rem;
        line-height: 1.8;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Input box */
    .stTextInput input {
        font-size: 1.2rem !important;
        padding: 1rem !important;
        border-radius: 10px !important;
    }
    
    /* Buttons */
    .stButton button {
        font-size: 1.2rem !important;
        padding: 0.8rem 2rem !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
    
    /* Warning box */
    .warning-box {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 1.1rem;
    }
    
    /* Sidebar */
    .css-1d391kg {
        padding: 2rem 1rem;
    }
    
    /* Metrics */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="big-title">🏥 Medical AI Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Powered by Llama 3.3 70B & The GALE Encyclopedia of Medicine</p>', unsafe_allow_html=True)

# Warning banner
st.markdown("""
    <div class="warning-box">
        ⚠️ <strong>Medical Disclaimer:</strong> This chatbot provides general medical information for educational purposes only. 
        Always consult qualified healthcare professionals for medical advice, diagnosis, or treatment.
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 📊 System Status")
    
    # Initialize components if not already done
    if not st.session_state.initialized:
        try:
            st.session_state.embeddings, st.session_state.docsearch = initialize_components()
            st.session_state.initialized = True
            st.success("✅ AI Components Loaded")
        except Exception as e:
            st.error(f"❌ Initialization Error: {str(e)}")
    else:
        st.success("✅ AI Components Ready")
    
    st.markdown("---")
    
    # Stats
    st.markdown("### 📈 Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Questions Asked", len(st.session_state.chat_history))
    with col2:
        st.metric("Model", "Llama 3.3")
    
    st.markdown("---")
    
    # Example questions
    st.markdown("### 💡 Try These Questions:")
    example_questions = [
        "What is diabetes?",
        "What are symptoms of hypertension?",
        "How is asthma treated?",
        "What causes migraine headaches?",
        "Explain the common cold"
    ]
    
    for q in example_questions:
        if st.button(q, key=f"example_{q}", use_container_width=True):
            st.session_state.current_question = q
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    
    st.markdown("---")
    
    # About section
    st.markdown("### ℹ️ About")
    st.info("""
    **Technology Stack:**
    - 🤖 Llama 3.3 70B (Groq)
    - 🔍 RAG Architecture
    - 📚 GALE Medical Encyclopedia
    - 🗄️ Pinecone Vector DB
    - 🐍 Python + Streamlit
    """)
    
    st.markdown("""
    **Developed by:** [Your Name]  
    **GitHub:** [Your Link]  
    **LinkedIn:** [Your Link]
    """)

# Main chat interface
st.markdown("## 💬 Ask Your Medical Question")

# Check if there's a question from example buttons
if 'current_question' in st.session_state:
    user_question = st.session_state.current_question
    del st.session_state.current_question
else:
    user_question = st.text_input(
        "Type your question here...",
        placeholder="e.g., What are the symptoms of diabetes?",
        label_visibility="collapsed",
        key="question_input"
    )

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    ask_button = st.button("🔍 Get Answer", use_container_width=True, type="primary")

# Process question
if (ask_button or user_question) and user_question:
    if st.session_state.initialized:
        with st.spinner("🤔 Thinking... (This may take a few seconds)"):
            answer, context = get_medical_answer(user_question, st.session_state.docsearch)
            
            # Add to chat history
            st.session_state.chat_history.append({
                "question": user_question,
                "answer": answer,
                "timestamp": datetime.now().strftime("%I:%M %p"),
                "context": context
            })

# Display chat history (most recent first)
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("## 📝 Conversation History")
    
    for i, chat in enumerate(reversed(st.session_state.chat_history)):
        # User question
        st.markdown(f"""
            <div class="user-message">
                <strong>👤 You ({chat['timestamp']}):</strong><br>
                {chat['question']}
            </div>
        """, unsafe_allow_html=True)
        
        # Bot answer
        st.markdown(f"""
            <div class="bot-message">
                <strong>🤖 Medical Assistant:</strong><br>
                {chat['answer']}
            </div>
        """, unsafe_allow_html=True)
        
        # Show context in expander
        with st.expander("📚 View Source Context"):
            st.text(chat['context'])
        
        if i < len(st.session_state.chat_history) - 1:
            st.markdown("---")
else:
    # Empty state
    st.markdown("""
        <div style='text-align: center; padding: 4rem 2rem; color: #64748b;'>
            <h2>👋 Welcome to Medical AI Assistant!</h2>
            <p style='font-size: 1.2rem; margin-top: 1rem;'>
                Ask any medical question to get started.<br>
                Try the example questions in the sidebar or type your own question above.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #64748b; padding: 2rem 0;'>
        <p style='font-size: 1rem;'>
            Made with ❤️ using Streamlit, LangChain, and Groq AI<br>
            <small>This is an educational project. Always consult healthcare professionals for medical advice.</small>
        </p>
    </div>
""", unsafe_allow_html=True)