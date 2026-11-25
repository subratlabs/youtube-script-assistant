from pydantic import BaseModel,Field
from enum import Enum




class Language(str, Enum):
    ENGLISH = "English"
    HINDI = "Hindi"
    HINGLISH = "Hinglish"

class TargetAudience(str, Enum):
    BEGINNERS = "Beginners"
    INTERMEDIATE = "Intermediate learners"
    PROFESSIONALS = "Professionals"
    STUDENTS = "Students"
    GENERAL = "General audience"    

class ContentType(str, Enum):
    EDUCATIONAL = "Educational"
    TUTORIAL = "Tutorial"
    STORYTELLING = "Storytelling"
    TECHNOLOGY = "Technology"
    PRODUCT_REVIEW = "Product Review"
    MOTIVATIONAL = "Motivational"
    EXPLAINER = "Explainer"

class Tone(str, Enum):
    FRIENDLY = "Friendly"
    CONVERSATIONAL = "Conversational"
    PROFESSIONAL = "Professional"
    FUNNY = "Funny"
    INFORMATIVE = "Informative"
    STORYTELLING = "Storytelling"

class VideoRequirements(BaseModel):
    topic: str = Field(min_length=3, max_length=200)
    target_audience: TargetAudience
    language: Language
    duration: int = Field(ge=1, le=15)
    content_type: ContentType
    tone: Tone
    instructions: str | None = Field(default= None, max_length= 1000)
