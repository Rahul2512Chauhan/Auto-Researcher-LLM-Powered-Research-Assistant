from llm.provider_router import LLMRouter

llm = LLMRouter(provider="groq")
res = llm.generate("Router is working. Reply with 'success'.")
print(res)
