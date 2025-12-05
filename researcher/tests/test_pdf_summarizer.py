from pipelines.pdf_summarizer import summarize_pdf_text

def test_pdf_summarizer():
    text = "This research paper introduces a novel transformer architecture that improves efficiency."
    result = summarize_pdf_text(text)
    print(result)

test_pdf_summarizer()
