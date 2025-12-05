import time
import re
from dataclasses import dataclass
from typing import List, Optional
import arxiv

from researcher.pipelines.semantic_reranker import rerank_papers_by_semantics
from researcher.models.paper import Paper
from researcher.pipelines.query_expander import expand_query

# --- Helpers ---
def _normalize_query(q: str) -> str:
    """
    Basic cleaning/normalization of user queries so arXiv search behaves better.
    Removes excessive whitespace and newlines.
    """
    if not q:
        return ""
    q = q.strip()
    q = re.sub(r"\s+", " ", q)
    return q


def _extract_arxiv_id(entry_id: str) -> Optional[str]:
    """
    entry_id typically looks like: 'http://arxiv.org/abs/2301.12345v1'
    Return '2301.12345v1' (full arXiv id including version).
    """
    if not entry_id:
        return None
    match = re.search(r"arxiv\.org\/abs\/(.+)$", entry_id)
    return match.group(1) if match else None


# --- Core fetcher ---
def fetch_arxiv_candidates(
    query: str,
    candidate_count: int = 25,
    retry_attempts: int = 3,
    pause_seconds: float = 1.0,
    categories: Optional[List[str]] = None,
    sort_by: arxiv.SortCriterion = arxiv.SortCriterion.Relevance,
    sort_order: arxiv.SortOrder = arxiv.SortOrder.Descending,
) -> List[Paper]:
    """
    Fetch candidate papers from arXiv based on a user query.
    Returns up to `candidate_count` Paper objects.

    Notes:
    - This function intentionally returns a larger candidate set (default 25)
      so that later semantic reranking can pick the best ones.
    - `categories` is optional; if provided, it will restrict the query.
    """

    query = _normalize_query(query)
    if not query:
        return []

    # Build arXiv query. If categories provided, append them as OR group.
    if categories:
        cat_filter = " OR ".join([f"cat:{c}" for c in categories])
        full_query = f"({query}) AND ({cat_filter})"
    else:
        full_query = query

    attempt = 0
    while attempt < retry_attempts:
        try:
            search = arxiv.Search(
                query=full_query,
                max_results=candidate_count,
                sort_by=sort_by,
                sort_order=sort_order,
            )

            client = arxiv.Client(num_retries=1)  # arxiv lib has internal attempts but we still wrap externally
            papers: List[Paper] = []

            for res in client.results(search):
                arxiv_id = _extract_arxiv_id(getattr(res, "entry_id", "") or "")
                pdf_url = getattr(res, "pdf_url", None) or None

                published_dt = getattr(res, "published", None)
                if published_dt and hasattr(published_dt, "strftime"):
                    published_str = published_dt.strftime("%Y-%m-%d")
                else:
                    published_str = ""
                paper = Paper(
                    title=getattr(res, "title", "").strip(),
                    summary=(getattr(res, "summary", "") or "").strip(),
                    authors=[a.name for a in getattr(res, "authors", [])],
                    published=published_str,
                    pdf_url=pdf_url,
                    arxiv_id=arxiv_id,
                    raw_entry=res.__dict__ if hasattr(res, "__dict__") else {},
                )
                papers.append(paper)

            return papers

        except Exception as exc:
            attempt += 1
            if attempt >= retry_attempts:
                # final failure — return empty list (caller can decide)
                print(f"[arxiv_fetcher] Failed after {attempt} attempts: {exc}")
                return []
            else:
                # brief backoff then retry
                print(f"[arxiv_fetcher] attempt {attempt} failed: {exc} — retrying in {pause_seconds}s")
                time.sleep(pause_seconds)

    return []  # fallback


# --- Small convenience wrapper used by higher-level API ---
def search_papers(
    query: str,
    n_results: int = 5,
    candidates: int = 25,
    categories: Optional[List[str]] = None
):
    """
    High-level hybrid search:
    1) Use LLM to expand the research query
    2) Fetch candidates from arXiv for each expansion
    3) Merge + deduplicate all papers
    4) Semantic re-rank to find the top results
    """

    # --- 1. Expand the query ---
    expanded_queries = [query] + expand_query(query, n=5)

    print("\n[Expanded Queries]")
    for q in expanded_queries:
        print(" -", q)

    all_candidates: List[Paper] = []

    # --- 2. Fetch candidates for each expanded query ---
    for q in expanded_queries:
        fetched = fetch_arxiv_candidates(
            query=q,
            candidate_count=candidates,
            categories=categories
        )
        all_candidates.extend(fetched)

    if not all_candidates:
        return []

    # --- 3. Deduplicate by arXiv ID ---
    unique = {}
    for p in all_candidates:
        if p.arxiv_id:
            unique[p.arxiv_id] = p

    deduped_list = list(unique.values())

    print(f"\n[Candidates before dedupe]: {len(all_candidates)}")
    print(f"[Candidates after dedupe]:  {len(deduped_list)}")

    # --- 4. Semantic re-ranking ---
    reranked = rerank_papers_by_semantics(query, deduped_list, top_k=n_results)

    return reranked