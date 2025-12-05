from typing import List
import numpy as np

from researcher.models.paper import Paper
from researcher.llm.embeddings import get_embedding

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Computes cosine similarity between two embedding vectors.
    """
    if a.size == 0 or b.size == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def rerank_papers_by_semantics(
    query: str,
    papers: List[Paper],
    top_k: int = 5
) -> List[Paper]:
    """
    Reranks arXiv papers based on semantic similarity using OpenAI embeddings.
    Returns top_k most relevant papers.
    """

    if not papers:
        return []

    # 1. Embed the query
    query_emb = np.array(get_embedding(query))

    scored_papers = []

    for paper in papers:
        # 2. Combine metadata for embedding
        combined_text = f"{paper.title}\n\n{paper.summary}"

        # 3. Get embedding for the paper
        paper_emb = np.array(get_embedding(combined_text))

        # 4. Compute similarity
        score = cosine_similarity(query_emb, paper_emb)

        scored_papers.append((score, paper))

    # 5. Sort papers by score (highest first)
    scored_papers.sort(reverse=True, key=lambda x: x[0])

    # 6. Return top_k
    return [p for _, p in scored_papers[:top_k]]