def get_insight_prompt(summary_text:str)->str:
    
    """
    Builds a prompt to extract insights from a give research summary.

    Args:
        summary_text(str): The research paper summary text.

    Returns :
        str : The full prompt to send to te LLM.

    """
    prompt = f"""
You are a research assistant specialized in summarizing and analyzing academic papers.

Given the following research summary, extract exactly 10 key insights. For each insight, explain:

1. What the insight is
2. Why it is significant (its impact or importance in context)

Format the output as JSON with this structure:
[
  {{
    "insight": "<concise statement of the insight>",
    "significance": "<why it matters>"
  }},
  ...
]

### Research Summary :

\"\"\"
{summary_text}
\"\"\"

Now list the 5 insights in JSON format:
"""

    return prompt