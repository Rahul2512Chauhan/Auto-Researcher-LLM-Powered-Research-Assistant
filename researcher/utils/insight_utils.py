import json
import re
from typing import List, Dict

def parse_insights(raw_text: str) -> List[Dict[str, str]]:
    """
    Parses raw insights text (numbered list) into a list of insights with
    'insight' and 'significance' fields.

    Assumes each insight is numbered like:
    1. Insight : <text>
       Significance : <text>
       Type : <label>

    Args:
        raw_text (str): Raw text output from Zephyr with numbered insights.

    Returns:
        List[Dict[str, str]]: List of insights with keys 'insight' and 'significance'.
    """
    insights = []
    
    # Find all numbered entries using regex
    pattern = r'\d+\.\s*Insight:\s*(.*?)\s*Significance:\s*(.*?)\s*Type:\s*(.*?)(?=\n\d+\.|$)'
    matches = re.findall(pattern, raw_text, re.DOTALL)
    

    if not matches:
        print("[Warning] Structured parsing failed. Trying fallback parsing...")
        # Fallback: handle cases without labeled fields
        fallback_pattern = r'\d+\.\s+(.*?)(?=\n\d+\.|$)'
        fallback_matches = re.findall(fallback_pattern, raw_text, re.DOTALL)
        for entry in fallback_matches:
            sentences = re.split(r'\.(?:\s+|\n)', entry.strip(), maxsplit=1)
            insight_text = sentences[0].strip() + '.' if sentences else ""
            significance = sentences[1].strip() if len(sentences) > 1 else ""
            insights.append({
                "insight": insight_text,
                "significance": significance,
                "type": "unspecified"
            })
    else:
        for insight, significance, insight_type in matches:
            insights.append({
                "insight": insight.strip(),
                "significance": significance.strip(),
                "type": insight_type.strip().lower()
            })

    return insights


def save_insights_to_json(insights: List[Dict[str, str]], filename: str):
    """
    Saves insights list to a JSON file.

    Args:
        insights (List[Dict[str, str]]): List of insights to save.
        filename (str): Output JSON filename.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(insights, f, indent=4, ensure_ascii=False)
        print(f"Insights saved to {filename}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")

def save_insights_to_md(insights: List[Dict[str, str]], filename: str):
    """
    Saves insights list to a Markdown file in a readable format.

    Args:
        insights (List[Dict[str, str]]): List of insights to save.
        filename (str): Output Markdown filename.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Extracted Insights\n\n")
            for i, item in enumerate(insights, start=1):
                f.write(f"## Insight {i}\n\n")
                f.write(f"**Insight:** {item['insight']}\n\n")
                if item['significance']:
                    f.write(f"**Significance:** {item['significance']}\n\n")
                f.write("---\n\n")
        print(f"Insights saved to {filename}")
    except Exception as e:
        print(f"Error saving Markdown file: {e}")


