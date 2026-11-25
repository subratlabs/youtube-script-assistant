from fastapi import APIRouter, HTTPException

from app.schemas.video import VideoRequirements
from app.schemas.titles import TitlesResponse
from app.services.gemini_service import generate_content
from app.services.prompt_service import create_titles_prompt

router = APIRouter()


@router.post("/api/generate-titles", response_model=TitlesResponse)
def generate_titles(data: VideoRequirements):

    prompt = create_titles_prompt(data)
    try:
        response = generate_content(prompt)

        
    except Exception:
        raise HTTPException(status_code=503, detail="Unable to generate titles right now. Please try again later.")
    
    titles = [
        title.strip()
        for title in response.splitlines()
        if title.strip()
    ]

    return {
        "titles": titles
    }