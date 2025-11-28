# CORRECT IMPORTS FOR YOUR VERSION:
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter  # CHANGED
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document  # CHANGED
from typing import List

print("✅ Using LangChain 1.0.8 compatible imports")

# Your functions remain the same...
def load_pdf_file(data):
    loader = DirectoryLoader(
        data,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )
    documents = loader.load()
    print(f"📚 Loaded {len(documents)} documents from PDFs")
    return documents

def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )
        )
    print(f"🔧 Filtered {len(minimal_docs)} documents")
    return minimal_docs

def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, 
        chunk_overlap=20
    )
    text_chunks = text_splitter.split_documents(extracted_data)
    print(f"✂️ Split into {len(text_chunks)} text chunks")
    return text_chunks

def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2'
    )
    print("🔤 HuggingFace embeddings loaded")
    return embeddings