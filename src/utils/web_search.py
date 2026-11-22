import os

from dotenv import load_dotenv
from tavily import TavilyClient

from schemas.research import ResearchFinding

load_dotenv()


def search_web(query: str, max_results: int = 8) -> list[ResearchFinding]:
    """Search the web and return source-backed findings."""

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError("TAVILY_API_KEY is missing. Add it to your .env file.")

    client = TavilyClient(api_key=api_key)
    response = client.search(
        query=query,
        topic="general",
        max_results=max_results,
        search_depth="basic",
    )

    findings: list[ResearchFinding] = []
    for result in response.get("results", []):
        url = result.get("url")
        if not url:
            continue

        findings.append(
            ResearchFinding(
                title=result.get("title") or "Untitled source",
                content=result.get("content") or "",
                source_url=url,
            )
        )

    return findings
