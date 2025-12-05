from researcher.pipelines.query_expander import expand_query

print("Testing query expansion...")

queries = expand_query("rag evals", n=5)

print("\nExpanded Queries:")
for q in queries:
    print("-", q)
