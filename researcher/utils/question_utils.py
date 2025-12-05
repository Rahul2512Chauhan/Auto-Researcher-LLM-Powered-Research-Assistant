import re
import json
from typing import List, Dict


def parse_questions(raw_output: str) -> List[Dict[str, str]]:
    """
    Parses a raw LLM output string into structured research questions and justifications.

    Args:
        raw_output (str): Numbered list of questions with justifications.

    Returns:
        List[Dict[str, str]]: List of {"question": ..., "justification": ...} entries.
    """
    if not isinstance(raw_output, str):
        raise ValueError("Expected a string for raw_output, got type: {}".format(type(raw_output)))

    raw_output = raw_output.strip()
    if not raw_output:
        return []

    pattern = r"\d+\.\s*(.+?)(?:\n|$)\s*(?:-|\u2013)?\s*(?:Why|Justification|Reason|This is|This)?[:\-]?\s*(.*?)(?=\n\d+\.|\Z)"
    matches = re.findall(pattern, raw_output, re.DOTALL)

    parsed_questions = []
    for question, justification in matches:
        parsed_questions.append({
            "question": question.strip(),
            "justification": justification.strip()
        })

    return parsed_questions


def save_questions_to_json(questions: List[Dict[str, str]], filename: str) -> None:
    """
    Saves a list of structured questions to a JSON file.

    Args:
        questions (List[Dict[str, str]]): List of questions.
        filename (str): Output JSON filename.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=4, ensure_ascii=False)


def save_questions_to_md(questions: List[Dict[str, str]], filename: str) -> None:
    """
    Saves a list of structured questions to a Markdown file.

    Args:
        questions (List[Dict[str, str]]): List of questions.
        filename (str): Output Markdown filename.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for i, item in enumerate(questions, 1):
            f.write(f"### {i}. {item['question']}\n")
            f.write(f"- **Justification**: {item['justification']}\n\n")
