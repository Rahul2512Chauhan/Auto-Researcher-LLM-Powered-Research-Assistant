import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List
from phase_1_setup.setup_zephyr import query_zephyr_locally  # ✅ Reusable model interface


def summarize_papers(paper_summaries: List[str]) -> str:
    """
    Summarizes multiple research paper abstracts into a single cohesive summary using local Zephyr.

    Args:
        paper_summaries (List[str]): A list of research paper abstracts.

    Returns:
        str: A cohesive paragraph summarizing the input abstracts.
    """
    if not paper_summaries:
        return "No paper summaries provided."

    combined_text = "\n\n".join(paper_summaries)

    system_prompt = (
        "You are a helpful AI assistant.\n"
        "Summarize the following research paper abstracts into a single long paragraph:"
    )

    return query_zephyr_locally(
        prompt=combined_text,
        system_prompt=system_prompt,
        temperature=0.5,
        max_tokens=500,
        log=False  # Set to True to debug prompt/response
    )

