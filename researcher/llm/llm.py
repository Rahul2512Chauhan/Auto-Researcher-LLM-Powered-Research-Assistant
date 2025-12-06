from researcher.llm.provider_router import LLMRouter

# Create a single global router instance
_llm_router = LLMRouter()


from typing import Optional

def generate(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
) -> str:
    """
    Universal LLM entrypoint for your entire application.
    Usage:
        from researcher.llm.llm import generate
        text = generate("Explain GraphRAG")
    """
    return _llm_router.generate(
        prompt,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
    )
