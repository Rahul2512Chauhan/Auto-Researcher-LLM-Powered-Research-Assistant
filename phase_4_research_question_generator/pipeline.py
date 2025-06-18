import sys
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phase_4_research_question_generator.question_generator import generate_research_question
from phase_4_research_question_generator.question_utils import save_questions_to_json, save_questions_to_md
from typing import List, Dict

def run_pipeline(
        insights: List[Dict[str, str]], 
        base_filename: str = "research_questions", 
        num_questions: int = 5,
        ) -> List[Dict[str, str]]:
    """
    Runs the full research question generation pipeline:
    - Generates questions from insights using local Zephyr
    - Saves them to JSON and Markdown
    - Returns the questions

    Args:
        insights (List[Dict[str, str]]): List of extracted insights from Phase 3.
        base_filename (str): Base filename for saving outputs.
        num_questions (int): Number of questions to generate.

    Returns:
        List[Dict[str, str]]: Research questions with justifications.
    """
    questions = generate_research_question(insights, num_questions=num_questions)

    # Save to JSON and Markdown
    save_questions_to_json(questions, f"{base_filename}.json")
    save_questions_to_md(questions, f"{base_filename}.md")

    return questions
