# researcher/tests/test_orchestrator.py
from researcher.agents.orchestrator import Orchestrator

print("\n=== TESTING ORCHESTRATOR ===")
orch = Orchestrator(reviewer_enabled=False)  # disable reviewer for faster runs in test
res = orch.run("Survey recent techniques for reducing hallucinations in RAG systems.", review_each_task=False)

print("\nRun Tasks:")
print(res.get("tasks"))
print("\nFinal state keys:")
print(list(res.get("state", {}).keys()))
