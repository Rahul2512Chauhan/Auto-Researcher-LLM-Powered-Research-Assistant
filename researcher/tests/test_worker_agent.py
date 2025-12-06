from researcher.agents.planner_agent import plan_research
from researcher.agents.worker_agent import WorkerAgent

print("\n=== TESTING WORKER AGENT ===")

query = "Survey recent techniques for reducing hallucinations in RAG systems."

tasks = plan_research(query)

worker = WorkerAgent()

state = {"query": query}

final_state = worker.run_plan(tasks, state)

print("\n=== FINAL STATE KEYS ===")
print(list(final_state.keys()))
