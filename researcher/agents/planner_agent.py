import json
from typing import List, Dict, Any

from researcher.llm.llm import generate


PLANNER_SYSTEM_PROMPT = """
You are an expert research planner AI.
Your job is to break a research query into a structured set of tasks.

Rules:
- RETURN ONLY VALID JSON. No explanation.
- JSON must be a list of task objects.
- Each task object must contain:
  - name: short task ID string
  - description: what this task does
  - required_inputs: list of inputs required
  - expected_outputs: list of outputs it produces
  - dependencies: list of task names this step depends on

- Use snake_case for "name".

- Do NOT include comments or text outside JSON.
"""


def plan_research(query: str) -> List[Dict[str, Any]]:
    """
    Calls Groq LLM and returns a list of structured tasks for the research workflow.
    """

    user_prompt = f"Generate a complete task plan for this research query:\n\n{query}"

    raw_output = generate(
        prompt=user_prompt,
        system_prompt=PLANNER_SYSTEM_PROMPT,
        temperature=0.2,
        max_tokens=800,
    )

    # Try to parse JSON safely
    try:
        tasks = json.loads(raw_output)
        if isinstance(tasks, list):
            return tasks
        else:
            print("[Planner] Output was not a list. Returning empty.")
            return []
    except Exception as e:
        print(f"[Planner] Failed to parse JSON: {e}\nRaw output:\n{raw_output}")
        return []
