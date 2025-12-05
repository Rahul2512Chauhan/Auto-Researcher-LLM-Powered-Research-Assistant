# tests/test_arxiv_fetcher.py
from data.arxiv_fetcher import search_papers

def test_search_basic():
    print("Running basic arXiv fetch test...")
    results = search_papers("retrieval-augmented generation", n_results=3, candidates=10)
    print(f"Got {len(results)} results")
    for i, p in enumerate(results, 1):
        print(f"\nResult {i}:")
        print("Title:", p.title)
        print("arXiv ID:", p.arxiv_id)
        print("PDF:", p.pdf_url)
        print("Authors:", ", ".join(p.authors))
        print("Published:", p.published)
        # Print a short summary snippet
        print("Summary snippet:", (p.summary or "")[:300])

if __name__ == "__main__":
    test_search_basic()
