from langgraph.graph import END, START, StateGraph

from agents.analyst import analyst_agent
from agents.critic import critic_agent
from agents.researcher import researcher_agent
from agents.orchestrator import initialize_workflow, orchestrator_agent
from schemas.state import ResearchState


def route_after_critic(state: ResearchState) -> str:
    """Allow at most one revision after the first critic review."""

    if not state.get("approved", False) and state.get("revision_count", 0) == 0:
        return "analyst"
    return END


def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("orchestrator", orchestrator_agent)
    graph.add_node("researcher", researcher_agent)
    graph.add_node("analyst", analyst_agent)
    graph.add_node("critic", critic_agent)

    graph.add_edge(START, "orchestrator")
    graph.add_edge("orchestrator", "researcher")
    graph.add_edge("researcher", "analyst")
    graph.add_edge("analyst", "critic")

    graph.add_conditional_edges(
        "critic",
        route_after_critic,
        {
            "analyst": "analyst",
            END: END,
        },
    )

    return graph.compile()


research_graph = build_graph()


def run_research(query: str) -> ResearchState:
    """Run the complete research workflow and return its final state."""

    initial_state = initialize_workflow(query)
    result = research_graph.invoke(initial_state)

    # If the critic rejects the revised draft, the revised draft is still returned,
    # with the critic's feedback visible to the user.
    if not result.get("final_report"):
        result["final_report"] = result.get("draft", "")

    return result
