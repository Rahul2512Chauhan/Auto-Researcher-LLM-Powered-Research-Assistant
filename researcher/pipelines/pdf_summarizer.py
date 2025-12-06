from researcher.llm.llm import generate

def summarize_pdf_text(paper_text: str) -> str:
    """
    Summarizes full text extracted from a research paper using the global LLM provider (Groq for now).
    """
    if not paper_text.strip():
        return "No paper text provided."

    prompt = f"""
You are an expert academic summarizer.

Your task is to summarize the following research paper text into a clear,
concise, and cohesive summary. Highlight the core contributions, methodology,
and findings. Avoid hallucinations and stay loyal to the original content.

TEXT:
{paper_text}

SUMMARY:
"""
    return generate(prompt)
