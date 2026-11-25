import json

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from app.schemas.visuals import VisualsRequest, VisualsResponse
from app.services.gemini_service import generate_content
from app.services.prompt_service import create_visuals_prompt


router = APIRouter()


@router.post("/api/generate-visuals", response_model=VisualsResponse)
def generate_visuals(data: VisualsRequest):

    prompt = create_visuals_prompt(data)

    try:
        response = generate_content(prompt, json_mode=True)
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to generate visual suggestions right now. Please try again later."
        )

    if not response.strip():
        raise HTTPException(
            status_code=503,
            detail="Gemini returned an empty response. Please try again later."
        )

    try:
        payload = json.loads(response)
        visuals_response = VisualsResponse.model_validate(payload)

    except (json.JSONDecodeError, ValidationError):
        raise HTTPException(
            status_code=502,
            detail="Gemini returned an invalid visual suggestions response."
        )

    return visuals_response