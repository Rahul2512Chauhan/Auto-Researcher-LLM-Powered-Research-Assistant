import os
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
MODEL_NAME = "text-embedding-3-small"


def get_embedding(text: str) -> List[float]:
    # Print header for each embedding call
    print("\n" + "="*60)
    print("🔍 Generating Embedding")
    print("-"*60)
    print(f"📝 Text Preview: {text[:80].replace('\n',' ')}")
    
    if not text or not text.strip():
        print("⚠️ EMPTY TEXT — returning empty embedding.")
        print("="*60 + "\n")
        return []

    try:
        response = client.embeddings.create(
            model=MODEL_NAME,
            input=text
        )

        emb = response.data[0].embedding
        print(f"📏 Embedding Size: {len(emb)}")
        print("✅ Status: Success")
        print("="*60 + "\n")

        return emb

    except Exception as e:
        print("❌ EMBEDDING ERROR:")
        print(str(e))
        print("="*60 + "\n")
        return []
