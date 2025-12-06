import os
from typing import List, Dict, Optional

from groq import Groq
from groq.types.chat import ChatCompletionUserMessageParam, ChatCompletionSystemMessageParam


class GroqProvider:
    """
    Wrapper around Groq API. 
    Clean, stable, LLM-agnostic interface used by the entire system.
    """

    DEFAULT_MODEL = "llama-3.1-8b-instant"

    def __init__(
        self,
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 400,
    ):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")

        self.client = Groq(api_key=api_key)
        self.model = model or self.DEFAULT_MODEL
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Unified Generation API.
        LangGraph & your agents will rely on this.
        """
        messages: List = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
            )

            content = response.choices[0].message.content
            return content.strip() if content is not None else ""

        except Exception as e:
            print(f"[GroqProvider] LLM Error: {e}")
            return f"[LLM ERROR] {e}"
