from schemas.state import ResearchState


def initialize_workflow(query: str) -> ResearchState:
    """Create the initial shared state for a research run."""

    cleaned_query = query.strip()
    if not cleaned_query:
        raise ValueError("Research query cannot be empty.")

    return {
        "query": cleaned_query,
        "findings": [],
        "draft": "",
        "critic_feedback": "",
        "approved": False,
        "revision_count": 0,
        "final_report": "",
        "error": "",
    }


def orchestrator_agent(state: ResearchState) -> dict:
    """Validate the incoming request and pass it to the researcher."""

    query = state.get("query", "").strip()
    if not query:
        raise ValueError("Orchestrator received an empty research query.")

    return {"query": query}
