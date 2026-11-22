import json

from langchain_core.messages import HumanMessage, SystemMessage

from agents.analyst import get_llm
from schemas.research import CriticReview
from schemas.state import ResearchState


def critic_agent(state: ResearchState) -> dict:
    """Evaluate the draft against the query and available evidence."""

    evidence = "\n\n".join(
        f"{item.title}\n{item.source_url}\n{item.content}"
        for item in state.get("findings", [])
    )

    system_prompt = """
You are a strict but fair reviewer of a short market research brief.

Check whether the draft:
- answers the user's research query;
- includes the required sections;
- makes claims supported by the supplied evidence;
- avoids invented statistics and unsupported competitor claims;
- includes source URLs;
- identifies important missing information;
- is clear and concise.

Return ONLY valid JSON with exactly these keys:
{
  "approved": true,
  "feedback": "Short explanation"
}

Set approved to false only when there is a meaningful issue that should be fixed.
Do not demand information that is absent from the evidence; the report can state
that information is missing.
"""

    user_prompt = f"""
Original query:
{state['query']}

Available evidence:
{evidence}

Draft to review:
{state.get('draft', '')}
"""

    response = get_llm().invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
    )

    raw = response.content
    if not isinstance(raw, str):
        raw = str(raw)

    # Parse JSON, including the occasional Markdown code fence returned by an LLM.
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```json").removeprefix("```").strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()

    try:
        data = json.loads(cleaned)
        review = CriticReview.model_validate(data)
    except Exception:
        # Fail safely: do not block the user from receiving the draft.
        review = CriticReview(
            approved=True,
            feedback=(
                "The critic response could not be parsed as JSON. "
                "The draft is being returned without a confirmed critic approval."
            ),
        )

    return {
        "approved": review.approved,
        "critic_feedback": review.feedback,
        "final_report": state.get("draft", ""),
    }
