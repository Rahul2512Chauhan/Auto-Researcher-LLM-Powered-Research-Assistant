from llm.llm import generate

def summarize_text(text: str) -> str:
    """
    Summarizes a block of text using the global LLM provider (Groq for now).
    """
    prompt = f"""
You are an expert academic summarizer.

Summarize the following text in a clear, structured, and factual way.
Avoid hallucinations. Preserve key arguments. Keep it concise.

TEXT:
{text}

SUMMARY:
"""
    return generate(prompt)
