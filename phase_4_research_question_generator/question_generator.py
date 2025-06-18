import sys
import os
from typing import List, Dict

# Add root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.prompts import ChatPromptTemplate
from phase_1_setup.setup_zephyr import query_zephyr_locally
import re

def generate_research_question(insights: List[Dict[str, str]], num_questions: int = 3) -> List[Dict[str, str]]:
    """
    Generates novel research questions using a local Zephyr model based on provided insights.

    Args:
        insights (List[Dict[str, str]]): List of insights with 'insight' and 'significance' keys.
        num_questions (int): Number of research questions to generate.

    Returns:
        List[Dict[str, str]]: List of questions with justifications.
    """

    if not insights:
        return [{"error": "No insights provided."}]

    # Combine insights into a readable string
    insight_block = "\n".join([
        f"{i+1}. Insight: {item['insight']}\n   Significance: {item['significance']}"
        for i, item in enumerate(insights)
    ])

    # Instruction for Zephyr
    system_prompt = (
        f"You are a research strategist. Based on the insights below, generate {num_questions} "
        f"novel and meaningful research questions that extend the current work. "
        f"For each question, briefly explain why it is important. Format the response as:\n\n"
        f"1. Question\nJustification: Explanation\n2. Question\nJustification: Explanation ..."
    )

    # Create LangChain-style prompt
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "{system_prompt}"),
        ("human", "{input}")
    ])

    rendered_prompt = prompt_template.format(
        system_prompt=system_prompt,
        input=insight_block
    )

    zephyr_output = query_zephyr_locally(
        prompt=rendered_prompt,
        system_prompt=""  # Already included above
    )

    return parse_output(zephyr_output)


def parse_output(output: str) -> List[Dict[str, str]]:
    """
    Parses numbered questions and their justifications from raw model output.

    Args:
        output (str): Raw output from Zephyr

    Returns:
        List[Dict[str, str]]: Cleanly split questions and justifications
    """
    # Regex to match question + justification pairs
    pattern = r"\d+\.\s+(.*?)\nJustification:\s+(.*?)(?=\n\d+\.|\Z)"
    matches = re.findall(pattern, output, re.DOTALL)

    results = []
    for question, justification in matches:
        results.append({
            "question": question.strip(),
            "justification": justification.strip()
        })

    return results
