from pipelines.summarizer import summarize_text

def test_summary():
    text = "Retrieval-Augmented Generation (RAG) improves factual accuracy by combining retrieval and generation."
    result = summarize_text(text)
    print(result)

test_summary()
