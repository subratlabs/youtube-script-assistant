from fastapi import APIRouter, HTTPException

from app.schemas.video import VideoRequirements
from app.schemas.hooks import HooksResponse
from app.services.gemini_service import generate_content
from app.services.prompt_service import create_hooks_prompt


router = APIRouter()

@router.post("/api/generate-hooks", response_model=HooksResponse)
def generate_hooks(data: VideoRequirements):

    prompt = create_hooks_prompt(data)

    try:
        response = generate_content(prompt)
    except Exception:
        raise HTTPException(
        status_code=503,
        detail="Unable to generate hooks right now. Please try again later."
        )

    hooks = [
        hook.strip()
        for hook in response.splitlines()
        if hook.strip()
    ]

    return {
        "hooks": hooks
    }