"""
section → which part of the video
visual → what should appear on screen
b_roll → supporting footage idea
on_screen_text → text displayed to viewers
"""


from pydantic import BaseModel, Field
from app.schemas.video import VideoRequirements


class VisualsRequest(VideoRequirements):
    selected_title: str = Field(min_length=3, max_length=200)
    script: str = Field(min_length=50, max_length=20000)

class VisualSuggestion(BaseModel):
    section: str
    visual: str
    b_roll: str
    on_screen_text: str


class VisualsResponse(BaseModel):
    visuals: list[VisualSuggestion]