from typing import Any, Dict, Union
from langchain_core.runnables import Runnable, RunnableConfig
from phase_1_setup.setup_zephyr import query_zephyr_locally

class ZephyrLLMWrapper(Runnable):
    """LangChain-compatible wrapper for querying local Zephyr model."""

    def __init__(self, temperature: float = 0.3, max_tokens: int = 500):
        self.temperature = temperature
        self.max_tokens = max_tokens

    from typing import Optional

    def invoke(self, input: Union[str, Dict[str, Any]], config: Optional["RunnableConfig"] = None, **kwargs) -> str:
        """
        LangChain expects invoke() to accept extra kwargs like 'stop', 'callbacks', etc.
        """
        if isinstance(input, dict):
            prompt = input.get("question") or input.get("input") or str(input)
        else:
            prompt = input

        # Ensure prompt is converted to string if it's a LangChain prompt object
        if hasattr(prompt, "to_string"):
            prompt = str(prompt)

        return query_zephyr_locally(
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
