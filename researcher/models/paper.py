from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Paper:
    title: str
    summary: str
    authors: List[str]
    published: str
    pdf_url: Optional[str]
    arxiv_id: Optional[str]
    raw_entry: dict
