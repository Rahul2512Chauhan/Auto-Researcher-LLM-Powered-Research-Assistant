from config import LLM_PROVIDER
from researcher.llm.groq_provider import GroqProvider
# from researcher.llm.local_zephyr import LocalZephyrProvider  # future


class LLMRouter:
    """
    Routes generation calls to the correct backend.
    """

    def __init__(self, provider: str | None = None):
        provider = provider or LLM_PROVIDER.lower()

        if provider == "groq":
            self.llm = GroqProvider()

        # elif provider == "local":
        #     self.llm = LocalZephyrProvider()

        else:
            raise ValueError(f"Unknown LLM provider: {provider}")

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Pass through to the selected provider.
        Extra kwargs allow system_prompt, temperature, etc.
        """
        return self.llm.generate(prompt, **kwargs)
