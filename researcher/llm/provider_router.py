from config import LLM_PROVIDER
from researcher.llm.groq_provider import GroqProvider
# LocalZephyrProvider will be added later

class LLMRouter:
    def __init__(self, provider: str | None = None):
        provider = provider or LLM_PROVIDER

        if provider == "groq":
            self.llm = GroqProvider()
        # Later we add:
        # elif provider == "local":
        #     self.llm = LocalZephyrProvider()
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def generate(self, prompt: str) -> str:
        return self.llm.generate(prompt)
