import arxiv
import textwrap


def fetch_arxiv_papers(query:str, max_results:int=5):
    """
    Fetch top `max_results` papers from arXiv for the given `query`.

    Args:
        query (str): Search query for arXiv papers
        max_results (int): Maximum number of papers to fetch (default: 5)
    
    Returns:
        list: List of paper dictionaries with title, summary, authors, etc.

    """
    
    try:
        # Filter categories for better topic alignment
        categories = ["cs.AI", "cs.CL", "cs.LG", "stat.ML", "cs.CY", "cs.HC"]
        category_filter = " OR ".join([f"cat:{cat}" for cat in categories])
        full_query = f"{query} AND ({category_filter})"

        # Create the search object with the full query
        search = arxiv.Search(
            query=full_query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )

    
        papers = []
        client = arxiv.Client()
        for result in client.results(search):
            paper = {
                "title": result.title,
                "summary": textwrap.fill(result.summary, width=80),
                "authors": [author.name for author in result.authors],
                "published": result.published.strftime("%Y-%m-%d"),
                "pdf_url": result.pdf_url
            }
            papers.append(paper)
        return papers
    
    except Exception as e:
        print(f"Error fetching papers: {e}")
        return []
    


def display_papers(papers):
    """
    Display fetched papers in a readable format.

    Args:
        papers (list): List of paper dictionaries
    """
    if not papers:
        print("No papers found.")
        return
    print(f"Found {len(papers)} papers:\n")

    summary_length = 2000  # Define the maximum length for the summary

    for i, paper in enumerate(papers, 1):
        print(f"\n📄 Paper {i}:")
        print(f"Title: {paper['title']}")
        print(f"Authors: {', '.join(paper['authors'])}")
        print(f"Published: {paper['published']}")
        print(f"PDF URL: {paper['pdf_url']}") 
        print(f"ArXiv ID: {paper.get('arxiv_id', 'N/A')}")

        summary = paper['summary'][:summary_length]
        if len(paper['summary']) > summary_length:
            summary += "..."
        
        wrapped_summary = textwrap.fill(summary, width=80, initial_indent="Summary: ", 
                                      subsequent_indent="         ")
        print(wrapped_summary)
        print("-" * 80)

