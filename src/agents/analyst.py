from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

from schemas.state import ResearchState

load_dotenv()


def get_llm() -> ChatOpenRouter:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is missing. Add it to your .env file.")

    model_name = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-v4.1-flash")
    return ChatOpenRouter(
        model=model_name,
        temperature=0.2,
        api_key=api_key,
    )


def analyst_agent(state: ResearchState) -> dict:
    """Create the first brief, or revise it using critic feedback."""

    findings_text = "\n\n".join(
        (
            f"Source title: {item.title}\n"
            f"URL: {item.source_url}\n"
            f"Evidence: {item.content}"
        )
        for item in state.get("findings", [])
    )

    is_revision = bool(state.get("critic_feedback"))
    if is_revision:
        task = f"""
Revise your previous research brief using the critic's feedback.

Previous draft:
{state.get('draft', '')}

Critic feedback:
{state.get('critic_feedback', '')}
"""
    else:
        task = "Create the initial research brief."

    system_prompt = """
You are a careful market research analyst.

Use only the supplied research findings. Do not invent facts, market sizes,
financial figures, dates, quotations, or competitor information. If evidence
is insufficient, explicitly say so.

Write a concise Markdown brief with these exact sections:
1. Summary
2. Competitors (include up to two only when relevant and supported)
3. Key observations
4. Sources
5. Missing information

For every factual point, make it clear which source supports it. In Sources,
include the actual URLs supplied in the evidence. Distinguish evidence from
interpretation. Keep the report useful and readable.
"""

    user_prompt = f"""
Research query:
{state['query']}

Research findings:
{findings_text}

{task}
"""

    response = get_llm().invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
    )

    draft = response.content
    if not isinstance(draft, str):
        draft = str(draft)

    updates = {"draft": draft}
    if is_revision:
        updates["revision_count"] = state.get("revision_count", 0) + 1

    return updates
