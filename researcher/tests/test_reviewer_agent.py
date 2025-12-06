from researcher.agents.reviewer_agent import ReviewerAgent

print("\n=== TESTING REVIEWER AGENT ===")

agent = ReviewerAgent()

sample_output = "RAG is a database indexing technique that improves LLM memory."

result = agent.review("test_task", sample_output)

print("\nReviewer Output:")
print(result)

assert "revised_output" in result
assert "issues_found" in result
assert "quality_score" in result

print("\n✅ Reviewer Agent Test Passed!")
