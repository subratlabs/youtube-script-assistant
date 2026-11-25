import json

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from app.schemas.description import DescriptionRequest, DescriptionResponse
from app.services.gemini_service import generate_content
from app.services.prompt_service import create_description_prompt


router = APIRouter()


@router.post("/api/generate-description", response_model=DescriptionResponse)
def generate_description(data: DescriptionRequest):

    prompt = create_description_prompt(data)

    try:
        response = generate_content(prompt, json_mode=True)
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to generate the description right now. Please try again later."
        )

    if not response.strip():
        raise HTTPException(
            status_code=503,
            detail="Gemini returned an empty response. Please try again later."
        )

    try:
        payload = json.loads(response)
        description_response = DescriptionResponse.model_validate(payload)

    except (json.JSONDecodeError, ValidationError):
        raise HTTPException(
            status_code=502,
            detail="Gemini returned an invalid description response."
        )

    return description_response