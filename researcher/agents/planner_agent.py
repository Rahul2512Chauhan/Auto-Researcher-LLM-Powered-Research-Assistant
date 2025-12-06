import json
from typing import List, Dict, Any
from researcher.memory.memory_store import MemoryStore
from researcher.llm.llm import generate

def plan_research(query: str):
    # Fetch memory relevant to this query
    mem = MemoryStore.search(query, top_k=5)

    # Extract documents nicely
    past_docs = []
    if mem and "documents" in mem:
        for group in mem["documents"]:
            for d in group:
                past_docs.append(d)

    memory_block = ""
    if past_docs:
        memory_block = "\n\nPAST KNOWLEDGE (from memory):\n" + "\n".join(
            f"- {p}" for p in past_docs
        )
ALLOWED_TASKS = [
    "search_papers",
    "summarize_papers",
    "extract_insights",
    "compare_insights",
    "generate_questions",
    "write_report"
]

PLANNER_PROMPT = f"""
You are an expert research workflow planner.

Given a user research query, create a step-by-step plan using ONLY these allowed tasks:

{ALLOWED_TASKS}

Rules:
- Output STRICT JSON. No commentary.
- Each task must include: name, inputs, outputs, dependencies.
- Use 4–6 tasks maximum.
- Tasks MUST be chosen only from ALLOWED_TASKS.
- The workflow must end with "write_report".

Example format:
{{
  "tasks": [
    {{
      "name": "search_papers",
      "inputs": ["query"],
      "outputs": ["papers"],
      "dependencies": []
    }},
    {{
      "name": "summarize_papers",
      "inputs": ["papers"],
      "outputs": ["summaries"],
      "dependencies": ["search_papers"]
    }}
  ]
}}
"""

