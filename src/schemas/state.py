from typing import TypedDict
from schemas.research import ResearchFinding

class ResearchState(TypedDict, total=False):
    """Shared state passed between LangGraph nodes."""

    query: str
    findings: list[ResearchFinding]
    draft: str
    critic_feedback: str
    approved: bool
    revision_count: int
    final_report: str
    error: str
