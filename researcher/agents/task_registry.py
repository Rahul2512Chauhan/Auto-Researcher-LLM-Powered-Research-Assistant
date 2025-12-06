# researcher/agents/task_registry.py

from researcher.data.arxiv_fetcher import search_papers
from researcher.pipelines.summarizer import summarize_text
from researcher.pipelines.insight_extractor import extract_insights
from researcher.agents.question_generator import generate_research_questions


# Map task names → actual Python functions
TASK_MAP = {
    "search_papers": search_papers,
    "semantic_rerank": search_papers,  # optional alias
    "summarize_papers": summarize_text,
    "extract_key_insights": extract_insights,
    "generate_research_questions": generate_research_questions,
}
