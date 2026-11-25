from pydantic import BaseModel, Field

from app.schemas.video import VideoRequirements


class RegenerationRequest(VideoRequirements):
    selected_title: str = Field(min_length=3, max_length=200)
    section_name: str = Field(min_length=2, max_length=100)
    current_section: str = Field(min_length=10, max_length=10000)
    full_script: str = Field(min_length=50, max_length=20000)


class RegenerationResponse(BaseModel):
    section_name: str
    regenerated_section: str