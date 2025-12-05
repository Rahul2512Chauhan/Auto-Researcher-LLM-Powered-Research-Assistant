# phase_5_rag_based_agent/rag_loader.py

# -------------------- Imports --------------------
from pathlib import Path
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    JSONLoader,
    UnstructuredMarkdownLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# -------------------- Document Loader --------------------
def load_document(file_path: str):
    """Load a single document based on its extension."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    ext = path.suffix.lower()
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path)
    elif ext == ".md":
        loader = UnstructuredMarkdownLoader(file_path)
    elif ext == ".json":
        loader = JSONLoader(file_path, jq_schema=".text", text_content=False)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
    
    return loader.load()

# -------------------- Chunking --------------------
def split_documents(documents, chunk_size: int = 1000, chunk_overlap: int = 150):
    """Split documents into manageable chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(documents)

# -------------------- Embedding Model --------------------
embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": "cpu"}  # change to "cuda" for GPU
)

# -------------------- FAISS Vector Store --------------------
def create_faiss_index_from_documents(documents, embeddings, save_path: str):
    """Create and save a FAISS index from document chunks."""
    db = FAISS.from_documents(documents, embeddings)
    db.save_local(save_path)
    return db

