```
🧠 Auto Researcher – LLM-Powered Research Assistant

🎥 Loom Demo

Watch how Auto-Researcher automates:

- Literature review 📚  
- Insight extraction 💡  
- Research question generation 🧠  
- Document Q&A with RAG 🤖  

## 🎥 Loom Demo

Watch how **Auto-Researcher** automates:

- Literature review 📚  
- Insight extraction 💡  
- Research question generation 🧠  
- Document Q&A with RAG 🤖  

[![Watch the demo video](https://raw.githubusercontent.com/Rahul2512Chauhan/Auto-Researcher-LLM-Powered-Research-Assistant/main/assets/loom_demo_thumbnail.png)](https://www.loom.com/share/e9210b1763db400882d05bb030ada533?sid=0f1efaeb-ad1f-4ee7-b2f2-732ed3f98598)



```
```
This project automates the research workflow using a locally-hosted Zephyr 7B model through a Streamlit interface.

It enables users to:

- 🔍 Search and summarize papers from arXiv
- 📄 Upload and analyze research PDFs
- 💡 Extract key insights from uploaded material
- ❓ Generate novel research questions with justifications
- 🤖 Ask questions to PDFs using a RAG-based document QA system
- 📦 Save output as JSON and Markdown

> ⚠️ This project does not rely on OpenAI or paid APIs. All LLM functionality runs locally.

```

```
> 💸 Zero-cost LLM: All features powered by a fully local Zephyr 7B model — no OpenAI or API costs!
```

```

🏗️ Architecture

Auto-Researcher – LLM-Powered Research Assistant
├── Phase 1: Local Zephyr Model Setup
├── Phase 2: arXiv Paper Search & Summarization
├── Phase 3: Insight Extraction from PDF
├── Phase 4: Research Question Generation (w/ justification)
└── Phase 5: RAG-based QA Agent (Ask questions to PDF content)

```

```

📁 Folder Structure

AUTO_RESEARCHER/
│
├── .vscode/ # VSCode config
├── faiss_index/ # Used in Phase 5 for retrieval
│
├── phase_1_setup/ # Zephyr 7B loading & initialization
│ ├── init.py
│ └── setup_zephyr.py
│
├── phase_2_lit_review/ # arXiv paper search & summarization
│   ├── init.py
│   └── arxiv_fetcher.py
│   └── pdf_reader.py
│   └── pdf_summarizer.py
│   └── summarizer.py
│
├── phase_3_insight_extractor/ # Insight extraction from papers
│   ├── init.py
│   └── insight_extractor.py
│   └── insight_utils.py
│   └── prompts.py
│   └── run_insight_pipeline.py
│
├── phase_4_research_question_generator/
│ ├── __init__.py
│ ├── question_generator.py
│ ├── question_utils.py
│ └── pipeline.py
│ 
├── phase_5_rag_based_agent/ # RAG-based PDF QA
│ ├── __init__.py
│ ├── rag_loader.py
│ ├── rag_index.py
│ ├── rag_qa_agent.py
│ └── llm_wrapper.py
│
├── ui.py # Streamlit frontend
├── requirements.txt # Python dependencies
├── .env # Environment variables (if any)
├── README.md # Project documentation
├── streamlit_output.json # Generated research questions
├── streamlit_output.md # Markdown version of above
├── 1706.03762v7.pdf # Sample PDF for testing

```

```
⚙️ Local Setup Instructions

git clone https://github.com/your-username/auto-researcher.git
cd auto-researcher

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
streamlit run ui.py
✅ Make sure your phase_1_setup/setup_zephyr.py loads the Zephyr 7B model correctly from disk.
```


```
🧠 Zephyr Model Info
Model: Zephyr-7B (Mistral-based)

Loaded: Locally, via HuggingFace Transformers

Why local?: To ensure full offline capability, privacy, and zero cost
```

```
🧠 Features by Phase:

Phase	Description
1	    Load Zephyr 7B model locally
2	    Search & summarize arXiv papers
3	    Extract insights from uploaded PDFs
4	    Generate research questions with justifications
5	    RAG-based document QA over uploaded PDFs

```

```
📜 License
For educational and research use only.
```
