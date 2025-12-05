from agents.rag_qa_agent import rag_answer

def test_rag():
    result = rag_answer("What is retrieval-augmented generation?")
    print(result)

test_rag()
