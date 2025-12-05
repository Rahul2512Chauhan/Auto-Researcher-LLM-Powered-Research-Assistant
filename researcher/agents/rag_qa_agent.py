from llm.llm import generate
from data.rag_index import retrieve_relevant_chunks

def rag_answer(query: str, top_k: int = 5) -> str:
    """
    RAG question answering agent.
    Retrieves relevant document chunks and answers using the global LLM provider.
    """
    if not query.strip():
        return "No query provided."

    # Retrieve context from vector store
    context_chunks = retrieve_relevant_chunks(query, top_k=top_k)

    if not context_chunks:
        context_text = "No relevant context found."
    else:
        context_text = "\n\n".join(context_chunks)

    # Build structured prompt
    prompt = f"""
You are an expert academic assistant.
Use ONLY the provided context to answer the user question.
If the answer is not in the context, say "The information is not available in the provided documents."

CONTEXT:
{context_text}

QUESTION:
{query}

ANSWER:
"""
    return generate(prompt)
