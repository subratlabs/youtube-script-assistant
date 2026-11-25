from pydantic import BaseModel, Field

from app.schemas.video import VideoRequirements


class DescriptionResponse(BaseModel):
    intro: str
    summary: str
    topics: list[str]
    keywords: list[str]
    hashtags: list[str]
    cta: str


class DescriptionRequest(VideoRequirements):
    selected_title: str = Field(min_length=3, max_length=200)
    script: str = Field(min_length=50, max_length=20000)