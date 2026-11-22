from pydantic import BaseModel, Field

class ResearchFinding(BaseModel):
    """One item of evidence returned by web search."""

    title: str = Field(description="Title of the web page or search result")
    content: str = Field(description="Relevant information extracted from the result")
    source_url: str = Field(description="Original URL of the source")


class CriticReview(BaseModel):
    """Structured decision made by the critic agent."""

    approved: bool = Field(description="Whether the draft is acceptable")
    feedback: str = Field(description="Reason for approval or requested improvements")