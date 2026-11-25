from fastapi import APIRouter, HTTPException

from app.schemas.video import VideoRequirements
from app.schemas.outline import OutlineResponse
from app.services.gemini_service import generate_content
from app.services.prompt_service import create_outline_prompt


router = APIRouter()


@router.post("/api/generate-outline", response_model=OutlineResponse)
def generate_outline(data: VideoRequirements):

    prompt = create_outline_prompt(data)

    try:
        response = generate_content(prompt)
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to generate the outline right now. Please try again later."
        )

    outline = [
        item.strip()
        for item in response.splitlines()
        if item.strip()
    ]

    return {
        "outline": outline
    }