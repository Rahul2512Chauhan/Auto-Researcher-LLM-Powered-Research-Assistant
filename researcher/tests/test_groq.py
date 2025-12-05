from llm.groq_provider import GroqProvider

llm = GroqProvider()

result = llm.generate("Say 'Groq integration working!'")
print(result)
