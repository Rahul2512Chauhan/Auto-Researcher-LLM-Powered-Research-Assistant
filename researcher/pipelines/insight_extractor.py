from llm.llm import generate

def extract_insights(text: str) -> str:
    """
    Extracts key insights from research text using the global LLM provider.
    """
    if not text.strip():
        return "No input text provided."

    prompt = f"""
You are an expert academic analyst.

Extract the **key insights**, **findings**, and **important contributions**
from the following research text. Present the insights as a structured,
bullet-point list. Keep them factual and concise. Avoid hallucinations.

TEXT:
{text}

INSIGHTS:
"""
    return generate(prompt)
