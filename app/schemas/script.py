from pydantic import BaseModel, Field
from app.schemas.video import VideoRequirements


class ScriptRequest(VideoRequirements):
    selected_title: str = Field(min_length=3, max_length=200)
    selected_hook: str = Field(min_length=5, max_length=1000)
    outline: list[str] = Field(min_length=1, max_length=15)


class ScriptResponse(BaseModel):
    script: str
    word_count: int
    estimated_duration: float


from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SavedScriptCreate(BaseModel):
    topic: str
    title: str
    content: str


class SavedScriptResponse(BaseModel):
    id: int
    topic: str
    title: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)