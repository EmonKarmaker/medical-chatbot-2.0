from dotenv import load_dotenv
import os
from src.helper import load_pdf_file, filter_to_minimal_docs, text_split, download_hugging_face_embeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
import time

load_dotenv()

print("🚀 Starting medical chatbot setup...")

# 1. Get API keys
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
if not PINECONE_API_KEY:
    raise ValueError("❌ PINECONE_API_KEY not found in environment variables")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# 2. Load and process data
print("📚 Loading PDF files...")
extracted_data = load_pdf_file(data='data/')
filter_data = filter_to_minimal_docs(extracted_data)
text_chunks = text_split(filter_data)
print(f"📄 Processed {len(text_chunks)} text chunks")

# 3. Get embeddings
print("🔤 Loading embeddings...")
embeddings = download_hugging_face_embeddings()

# Test embedding dimension
test_embed = embeddings.embed_query("medical test")
print(f"📏 Embedding dimension: {len(test_embed)}")

# 4. Initialize Pinecone
print("🌲 Connecting to Pinecone...")
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medical-chatbot"

# 5. Create or connect to index
existing_indexes = [index.name for index in pc.list_indexes()]
if index_name in existing_indexes:
    print(f"✅ Using existing index: {index_name}")
else:
    print(f"🆕 Creating new index: {index_name}")
    pc.create_index(
        name=index_name,
        dimension=384,  # Must match your embedding model!
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    print("⏳ Waiting for index to initialize...")
    time.sleep(30)

# 6. Create vector store
print("🗂️ Creating vector store...")
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    embedding=embeddings,
    index_name=index_name
)

print("🎉 Medical chatbot setup completed successfully!")