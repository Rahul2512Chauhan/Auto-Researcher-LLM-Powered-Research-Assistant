from typing import List
from researcher.llm.llm import generate

def _parse_list(text: str) -> List[str]:
    """
    Parses a numbered or bulleted list from the LLM output.
    Example:
        1. item
        2. item
    Returns clean list of items.
    """
    lines = text.strip().split("\n")
    cleaned = []

    for line in lines:
        # remove leading numbering or bullet
        line = line.strip()
        line = line.lstrip("-•* ")

        # remove "1." or "2)"
        line = line.split(".", 1)[-1] if line[:2].isdigit() else line
        line = line.split(")", 1)[-1] if ")" in line[:4] else line

        line = line.strip()
        if len(line) > 2:
            cleaned.append(line)

    return cleaned


def expand_query(user_query: str, n: int = 5) -> List[str]:
    """
    Expands a user query into several semantically related academic queries.
    Uses Groq LLM (llama-3.1-8b-instant) via global `generate()`.
    """
    
    prompt = f"""
You are an expert research assistant.

Expand the following research query into {n} related search queries.
Use technical terminology, synonyms, evaluation language, and adjacent topics.
Avoid generic or irrelevant expansions.

Return ONLY a numbered list.

Query: "{user_query}"
"""

    response = generate(prompt)

    expanded = _parse_list(response)

    # fallback — ensure at least the original query is included
    if not expanded:
        expanded = [user_query]

    return expanded
