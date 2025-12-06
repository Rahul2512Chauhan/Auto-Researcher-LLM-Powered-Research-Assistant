from researcher.llm.llm import generate

def generate_research_questions(text: str) -> str:
    """
    Generates high-quality research questions based on input text
    using the global LLM provider (Groq for now).
    """
    if not text.strip():
        return "No input text provided."

    prompt = f"""
You are an expert academic researcher.

Based on the following text, generate **high-quality, non-trivial research questions**.
They should be:
- specific
- novel
- relevant
- technically meaningful
- grounded in the provided content

TEXT:
{text}

Generate 5–7 strong research questions.

QUESTIONS:
"""
    return generate(prompt)
