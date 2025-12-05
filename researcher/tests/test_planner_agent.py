from researcher.agents.planner_agent import plan_research

print("\n=== TESTING PLANNER AGENT ===")

query = "Survey recent techniques for reducing hallucinations in RAG systems."

tasks = plan_research(query)

print("\nGenerated Tasks:")
for t in tasks:
    print("-", t["name"])
