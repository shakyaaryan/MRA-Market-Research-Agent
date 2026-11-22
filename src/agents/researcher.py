from schemas.research import ResearchFinding
from utils.web_search import search_web
from schemas.state import ResearchState


def researcher_agent(state: ResearchState) -> dict:
    """Collect evidence from web search for the user's topic."""

    query = state["query"]
    findings = search_web(query, max_results=8)

    if not findings:
        raise RuntimeError(
            "The search provider returned no usable results. Try a more specific query."
        )

    return {"findings": findings}
