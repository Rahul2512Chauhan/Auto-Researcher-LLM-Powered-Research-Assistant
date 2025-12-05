from researcher.llm.provider_router import LLMRouter

# Initialize one router (Groq for now)
llm = LLMRouter()

def generate(prompt: str) -> str:
    """
    Global simple LLM access.
    Usage: from auto_researcher.llm.llm import generate
    """
    return llm.generate(prompt)
