import json
from researcher.llm.llm import generate

class ReviewerAgent:
    """
    Reviews outputs produced by WorkerAgent.
    Checks for hallucinations, factual issues, and improves clarity.
    """

    def __init__(self):
        pass

    def review(self, task_name: str, output: str) -> dict:
        prompt = f"""
You are an expert research reviewer.

Your job is to analyze the result of a task performed by a research agent.

TASK NAME: {task_name}

OUTPUT TO REVIEW:
\"\"\"
{output}
\"\"\"

Analyze the output carefully and identify:
1. Possible factual errors
2. Any hallucinations
3. Missing citations
4. Weak reasoning or unclear structure

Then produce an improved and corrected version.

Return ONLY valid JSON with this exact structure:

{{
  "revised_output": "Improved version here...",
  "issues_found": ["issue1", "issue2"],
  "quality_score": 0.0 to 1.0
}}
"""

        response = generate(prompt)

        # Ensure JSON parsing robustness
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "revised_output": output,
                "issues_found": ["Reviewer failed to parse JSON"],
                "quality_score": 0.3
            }
