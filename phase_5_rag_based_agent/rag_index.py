# phase_5_rag_based_agent/rag_index.py

# ------------ Imports and Constants ------------
import os
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Constants
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
FAISS_DIR = "phase_5_rag_based_agent/vectorstore"
INDEX_FAISS_PATH = os.path.join(FAISS_DIR, "index.faiss")
INDEX_METADATA_PATH = os.path.join(FAISS_DIR, "index.pkl")


# ------------ Chunk Documents ------------
def chunk_documents(documents: List[Document]) -> List[Document]:
    """
    Splits documents into smaller chunks using recursive splitting.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_documents(documents)


# ------------ Embedding Model Loader ------------
def get_embedding_model():
    """
    Load the consistent HuggingFace embedding model.
    """
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"}  # Use "cuda" if GPU is available
    )


# ------------ Build and Save FAISS Index ------------
def build_and_save_faiss_index(chunks: List[Document]):
    """
    Create and save a FAISS vectorstore from document chunks.
    """
    os.makedirs(FAISS_DIR, exist_ok=True)
    embedding_model = get_embedding_model()
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    vectorstore.save_local(FAISS_DIR)
    print(f"[✔] FAISS index saved at: {FAISS_DIR}")


# ------------ Load FAISS Index ------------
def load_faiss_index():
    """
    Load FAISS vectorstore using the same embedding model.
    """
    try:
        embedding_model = get_embedding_model()
        return FAISS.load_local(
            FAISS_DIR,
            embeddings=embedding_model,
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        print(f"[!] Error loading FAISS index: {e}")
        return None

