# researcher/memory/memory_store.py
from typing import Any, Dict, List, Optional
import os
import uuid
import traceback

try:
    import chromadb
    from chromadb.config import Settings
except Exception as e:
    chromadb = None  # will raise later if used

from researcher.llm.embeddings import get_embedding


DEFAULT_PERSIST_DIR = os.path.join(os.getcwd(), "researcher_memory_db")


class MemoryStore:
    """
    Persistent vector memory using ChromaDB (duckdb+parquet backend).
    Collections:
      - summaries
      - insights
      - questions
      - citations
    """

    def __init__(self, persist_directory: Optional[str] = None):
        if chromadb is None:
            raise ImportError(
                "chromadb is not installed. Install it with: pip install chromadb"
            )

        self.persist_directory = persist_directory or DEFAULT_PERSIST_DIR
        os.makedirs(self.persist_directory, exist_ok=True)

        # Chroma 0.5+ config
        settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=self.persist_directory,
        )

        try:
            self.client = chromadb.Client(settings)
        except Exception:
            print("[MemoryStore] Persistent backend failed, switching to in-memory.")
            self.client = chromadb.Client()

        # initialize collections
        self._collections: Dict[str, Any] = {}
        for col in ("summaries", "insights", "questions", "citations"):
            self._collections[col] = self._get_or_create(col)

    def _get_or_create(self, name: str):
        try:
            return self.client.get_or_create_collection(name=name)
        except Exception:
            return self.client.create_collection(name=name)

    def list_collections(self) -> List[str]:
        try:
            return [c.name for c in self.client.list_collections()]
        except:
            return list(self._collections.keys())

    def add(
        self,
        category: str,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
        id: Optional[str] = None,
    ) -> str:
        if category not in self._collections:
            raise ValueError(f"Unknown collection: {category}")

        metadata = metadata or {}
        doc_id = id or metadata.get("id") or str(uuid.uuid4())

        emb = get_embedding(text)
        if not emb:
            raise ValueError("Failed to compute embedding for text.")

        try:
            self._collections[category].add(
                ids=[doc_id],
                documents=[text],
                metadatas=[metadata],
                embeddings=[emb],
            )
            return doc_id
        except Exception as e:
            print(f"[MemoryStore] Error adding document: {e}")
            traceback.print_exc()
            raise

    def upsert(self, category: str, id: str, text: str, metadata: Optional[Dict[str, Any]] = None):
        if category not in self._collections:
            raise ValueError(f"Unknown collection: {category}")

        metadata = metadata or {}
        emb = get_embedding(text)

        try:
            self._collections[category].upsert(
                ids=[id],
                documents=[text],
                metadatas=[metadata],
                embeddings=[emb],
            )
            return id
        except Exception as e:
            print(f"[MemoryStore] Error in upsert: {e}")
            traceback.print_exc()
            raise

    def query(
        self,
        category: str,
        text: Optional[str] = None,
        top_k: int = 5,
    ):
        if category not in self._collections:
            raise ValueError(f"Unknown collection: {category}")

        try:
            if text:
                emb = get_embedding(text)
                if not emb:
                    return {"documents": [], "metadatas": [], "distances": []}

                return self._collections[category].query(
                    query_embeddings=[emb],
                    n_results=top_k,
                    include=["documents", "metadatas", "distances"],
                )

            # no text → return default top-k
            return self._collections[category].query(
                n_results=top_k,
                include=["documents", "metadatas", "distances"],
            )

        except Exception as e:
            print(f"[MemoryStore] Query failed: {e}")
            traceback.print_exc()
            return {"documents": [], "metadatas": [], "distances": []}

    def get(self, category: str, id: str):
        if category not in self._collections:
            raise ValueError(f"Unknown collection: {category}")

        try:
            return self._collections[category].get(ids=[id])
        except Exception as e:
            print(f"[MemoryStore] Get failed: {e}")
            traceback.print_exc()
            return None

    def delete(self, category: str, id: str) -> bool:
        if category not in self._collections:
            raise ValueError(f"Unknown collection: {category}")

        try:
            self._collections[category].delete(ids=[id])
            return True
        except Exception as e:
            print(f"[MemoryStore] Delete failed: {e}")
            traceback.print_exc()
            return False
