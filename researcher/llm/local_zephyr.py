import requests
import json
from typing import Optional, Union

def query_zephyr_locally(
    prompt: Union[str, object],
    model: str = "zephyr",
    system_prompt: Optional[str] = "",
    temperature: float = 0.7,
    max_tokens: int = 512,
    stream: bool = False,
    log: bool = False
) -> str:
    """
    Generic interface for querying a local Zephyr model via Ollama.

    Args:
        prompt (str or PromptValue): The user-level task or instruction.
        model (str): The Ollama model name (default: "zephyr").
        system_prompt (str, optional): Optional system-level instruction.
        temperature (float): Generation temperature for randomness (default: 0.7).
        max_tokens (int): Max tokens to generate in the response (default: 512).
        stream (bool): Whether to stream output from model (currently False).
        log (bool): If True, print the prompt and response for debugging.

    Returns:
        str: Model-generated response or error message.
    """
    # Handle LangChain's PromptValue or custom objects safely
    prompt_str = str(prompt) if hasattr(prompt, "to_string") else str(prompt)
    combined_prompt = f"{system_prompt.strip()}\n\n{prompt_str.strip()}" if system_prompt else prompt_str.strip()

    payload = {
        "model": model,
        "prompt": combined_prompt,
        "temperature": temperature,
        "stream": stream,
        "options": {
            "num_predict": max_tokens
        }
    }

    if log:
        print("\n[🔧 Prompt Sent to Zephyr]")
        print(combined_prompt)
        print("-" * 60)

    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        response.raise_for_status()
        output = response.json().get("response", "[No 'response' field in JSON]")

        if log:
            print("[📨 Zephyr's Response]")
            print(output)
            print("=" * 60)

        return output

    except requests.exceptions.RequestException as e:
        return f"[Zephyr connection error] {e}"
