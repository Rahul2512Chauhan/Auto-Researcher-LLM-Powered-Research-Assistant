import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from phase_1_setup.setup_zephyr import query_zephyr_locally

from typing import Optional

def summarize_pdf_text(paper_text: str) -> str:
    """
    Summarizes full text extracted from a research paper using local Zephyr.

    Args:
        paper_text (str): The extracted text content from a PDF.

    Returns:
        str: A concise summary.
    """
    if not paper_text.strip():
        return "No paper text provided."

    system_prompt = (
        "You are a helpful research assistant.\n"
        "Summarize the following research paper into a single clear, concise, and cohesive paragraph:"
    )

    return query_zephyr_locally(
        prompt=paper_text,
        temperature=0.5,
        max_tokens=500,
        log=False
    )
