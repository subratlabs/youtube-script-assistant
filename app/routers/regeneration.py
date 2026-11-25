from fastapi import APIRouter, HTTPException

from app.schemas.regeneration import (
    RegenerationRequest,
    RegenerationResponse
)
from app.services.gemini_service import generate_content
from app.services.prompt_service import create_regeneration_prompt


router = APIRouter()


@router.post(
    "/api/regenerate-section",
    response_model=RegenerationResponse
)
def regenerate_section(data: RegenerationRequest):

    prompt = create_regeneration_prompt(data)

    try:
        response = generate_content(prompt)
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to regenerate the section right now. Please try again later."
        )

    if not response.strip():
        raise HTTPException(
            status_code=503,
            detail="Gemini returned an empty response. Please try again later."
        )

    return {
        "section_name": data.section_name,
        "regenerated_section": response.strip()
    }