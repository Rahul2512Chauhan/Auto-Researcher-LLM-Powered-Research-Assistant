import sys
import os

# Enable import from parent directories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from phase_1_setup.setup_zephyr import query_zephyr_locally


def extract_insights(summary_text: str, num_insights: int = 5) -> str:
    """
    Extracts key insights from a summary using the local Zephyr model.

    Args:
        summary_text (str): The summary from which to extract insights.
        num_insights (int): Number of insights to extract (default = 5).

    Returns:
        str: The extracted insights in a numbered list format.
    """

    if not summary_text.strip():
        return "[Error] Summary text is empty."

    system_prompt = (
        f"You are an academic assistant.\n"
        f"From the summary below, extract exactly {num_insights} key insights.\n"
        f"For each, include:\n"
        f"- The insight (1-2 sentences)\n"
        f"- Its significance\n"
        f"- Type: key_point, statistic, trend, or novel_idea\n\n"
        f"Format:\n"
        f"1. Insight: ...\n"
        f"   Significance: ...\n"
        f"   Type: ...\n"
    )

    return query_zephyr_locally(
        prompt=summary_text,
        system_prompt=system_prompt,
        temperature=0.5,
        max_tokens=700,
        log=False
    )



