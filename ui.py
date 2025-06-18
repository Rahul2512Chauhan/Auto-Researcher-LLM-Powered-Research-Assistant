import streamlit as st
import tempfile
import os
import sys

# Add project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

# ----------- Phase 2 + 3 Modules -----------
from phase_2_lit_review.arxiv_fetcher import fetch_arxiv_papers
from phase_2_lit_review.pdf_reader import extract_text_from_pdf
from phase_2_lit_review.pdf_summarizer import summarize_pdf_text
from phase_2_lit_review.summarizer import summarize_papers
from phase_3_insight_extractor.insight_extractor import extract_insights
from phase_3_insight_extractor.insight_utils import parse_insights

# ----------- Phase 5 (RAG Agent) -----------
from phase_5_rag_based_agent.rag_loader import load_document
from phase_5_rag_based_agent.rag_index import chunk_documents, build_and_save_faiss_index, load_faiss_index
from phase_5_rag_based_agent.rag_qa_agent import answer_query

# ----------- Streamlit Page Setup -----------
st.set_page_config(page_title="Auto Researcher", layout="wide")
st.title("📚 Auto Researcher — Literature Review, Insights & QA")

st.markdown("""
This app allows you to:
- 🔍 Search and summarize papers from **arXiv**
- 📄 Upload and summarize a **PDF**
- 💡 Extract meaningful **insights** from summaries
- 🧪 Generate Research Questions from Insights   
- 🤖 Ask questions from **uploaded documents using RAG**
""")

# ----------- Init Session State -----------
if "last_summary" not in st.session_state:
    st.session_state.last_summary = ""
if "rag_data" not in st.session_state:
    st.session_state.rag_data = {"index": None}

# ----------- Tab 1: arXiv Search & Summarize -----------
def summarize_arxiv_flow():
    st.header("🔍 Search and Summarize arXiv Papers")

    topic = st.text_input("Enter search topic for arXiv papers:")
    num_papers = st.slider("Number of papers to fetch", 1, 5, 3)

    if st.button("Fetch & Summarize Papers"):
        if not topic.strip():
            st.error("Please enter a valid topic.")
            return

        with st.spinner("Fetching papers from arXiv..."):
            papers = fetch_arxiv_papers(topic, max_results=num_papers)

        if not papers:
            st.warning("No papers found.")
            return

        st.success(f"Fetched {len(papers)} papers.")
        for i, paper in enumerate(papers, 1):
            st.markdown(f"**{i}. {paper['title']}**")
            st.markdown(f"*Authors:* {', '.join(paper['authors'])}")
            st.markdown(f"*Published:* {paper['published']}")
            st.markdown(f"[PDF Link]({paper['pdf_url']})")
            st.markdown(f"> {paper['summary'][:300]}...")
            st.markdown("---")

        abstracts = [p['summary'] for p in papers]
        with st.spinner("Generating combined summary..."):
            combined_summary = summarize_papers(abstracts)

        st.subheader("📝 Combined Summary")
        st.write(combined_summary)
        st.session_state.last_summary = combined_summary

# ----------- Tab 2: Upload & Summarize PDF -----------
def summarize_pdf_flow():
    st.header("📄 Upload PDF and Summarize")

    uploaded_pdf = st.file_uploader("Upload a research paper PDF", type=["pdf"])
    if uploaded_pdf is None:
        st.info("Upload a PDF to extract and summarize.")
        return

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_pdf.read())
        tmp_pdf_path = tmp_file.name

    try:
        with st.spinner("Extracting full text..."):
            full_text = extract_text_from_pdf(tmp_pdf_path)
    finally:
        os.remove(tmp_pdf_path)

    if not full_text or full_text.startswith("Error"):
        st.error(f"Failed to extract text: {full_text}")
        return

    st.success("Extracted text from PDF successfully.")
    st.write(f"Total characters extracted: {len(full_text)}")

    if st.button("Summarize PDF"):
        with st.spinner("Summarizing PDF..."):
            summary = summarize_pdf_text(full_text)

        st.subheader("📝 PDF Summary")
        st.write(summary)
        st.session_state.last_summary = summary

# ----------- Tab 3: Insight Extraction -----------
def insight_extraction_flow():
    st.header("💡 Generate Insights from Summary")

    summary_input = st.text_area(
        "Paste the summary below (auto-filled if available):",
        height=250,
        value=st.session_state.last_summary
    )
    num_insights = st.slider("How many insights to extract?", 3, 10, 5)

    if st.button("Extract Insights"):
        if not summary_input or not summary_input.strip():
            st.error("Please enter a summary.")
            return

        with st.spinner("Extracting insights..."):
            raw_output = extract_insights(summary_input, num_insights=num_insights)

        st.subheader("📄 Raw Output")
        st.code(raw_output)

        with st.spinner("Parsing insights..."):
            parsed = parse_insights(raw_output)

        st.subheader("✅ Parsed Insights")
        st.session_state.parsed_insights = parsed  # ✅ Save to session state

        for i, item in enumerate(parsed, 1):
            st.markdown(f"**{i}. Insight:** {item['insight']}")
            st.markdown(f"- **Significance:** {item['significance']}")
            st.markdown("---")


# ----------- Tab 4: Research Question Generator ----------
from phase_4_research_question_generator.pipeline import run_pipeline

def research_question_generator_tab():
    st.header("🧪 Generate Research Questions from Insights")

    insights = []
    use_auto = False

    # Step 1: Auto-fill from Tab 3 if available
    if "parsed_insights" in st.session_state:
        st.success("✅ Auto-filled insights from previous tab.")
        insights = st.session_state.parsed_insights
        use_auto = True

    if not use_auto:
        # Unique key added here 👇
        num_insights = st.number_input(
            "Number of insights",
            min_value=1,
            max_value=10,
            value=3,
            key="manual_num_insights"
        )
        for i in range(num_insights):
            insight = st.text_area(f"Insight #{i+1}", key=f"insight_{i}")
            significance = st.text_area(f"Significance #{i+1}", key=f"significance_{i}")
            if insight.strip() and significance.strip():
                insights.append({"insight": insight.strip(), "significance": significance.strip()})

    # Step 2: Number of questions
    num_questions = st.number_input(
        "Number of questions to generate",
        min_value=1,
        max_value=10,
        value=3,
        key="num_questions_to_generate"
    )

    # Step 3: Generate questions
    if st.button("🚀 Generate Research Questions"):
        if not insights:
            st.warning("Please provide at least one complete insight + significance pair.")
        else:
            with st.spinner("Thinking with Zephyr..."):
                questions = run_pipeline(insights, base_filename="streamlit_output", num_questions=num_questions)

            st.success("Research questions generated!")
            st.markdown("### 📌 Output Questions")
            for i, q in enumerate(questions, 1):
                st.markdown(f"**{i}. {q['question']}**")
                st.markdown(f"- *Justification:* {q['justification']}")



# ----------- Tab 5: RAG QA on Uploaded PDF -----------
def rag_qa_flow():
    st.header("❓ Ask Questions from Your PDF (RAG)")

    uploaded_pdf = st.file_uploader("Upload PDF for RAG QA", type=["pdf"], key="rag_pdf")
    if uploaded_pdf:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_pdf.read())
            tmp_pdf_path = tmp_file.name

        with st.spinner("Indexing document with FAISS..."):
            docs = load_document(tmp_pdf_path)
            chunks = chunk_documents(docs)
            build_and_save_faiss_index(chunks)
            index = load_faiss_index()
            st.session_state.rag_data["index"] = index

        os.remove(tmp_pdf_path)
        st.success("Document indexed for QA.")

    if st.session_state.rag_data.get("index"):
        question = st.text_input("Ask a question based on the uploaded PDF:")
        if st.button("Get Answer"):
            with st.spinner("Retrieving answer..."):
                answer = answer_query(
                    query=question,
                    retriever=st.session_state.rag_data["index"].as_retriever()
                )
            st.subheader("🧠 Answer")
            st.write(answer)

# ----------- Main App Entry -----------
def main():
    tab1, tab2, tab3, tab4 , tab5= st.tabs([
        "arXiv Search", 
        "Upload PDF Summary", 
        "Extract Insights", 
        "Research Question Generator",
        "RAG QA from PDF"
    ])
    with tab1: summarize_arxiv_flow()
    with tab2: summarize_pdf_flow()
    with tab3: insight_extraction_flow()
    with tab4: research_question_generator_tab()
    with tab5: rag_qa_flow()

if __name__ == "__main__":
    main()
