from researcher.data.arxiv_fetcher import search_papers

print("TEST FILE LOADED")

papers = search_papers("rag evals", n_results=5, candidates=15)


print("\nFinal Papers:")
for i, p in enumerate(papers, 1):
    print(f"{i}. {p.title}")
