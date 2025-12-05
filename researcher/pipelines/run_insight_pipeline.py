import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.insight_extractor import extract_insights
from utils.insight_utils import parse_insights , save_insights_to_json , save_insights_to_md
def run_pipeline(summary_text: str, base_filename: str ="insights" , num_insights: int = 5 ):
    """
    Runs the full insight extraction pipeline:
    - Generate insights using local Zephyr
    - Parse the insights
    - Save to .json and .md

    Args:
        summary_text (str): The input summary from which to extract insights.
        base_filename (str): Base name for output files.
        num_insights (int): Number of insights to extract.
    """
    print("Extracting insights from summary using Zephyr...")
    raw_output = extract_insights(summary_text, num_insights=num_insights)
    
    print("\nParsing insights...")
    parsed = parse_insights(raw_output)

    print("\nSaving insights to JSON and Markdown...")
    save_insights_to_json(parsed, f"{base_filename}.json")
    save_insights_to_md(parsed, f"{base_filename}.md")
    print("Done.")
