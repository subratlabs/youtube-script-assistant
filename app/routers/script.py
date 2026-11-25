from fastapi import APIRouter, HTTPException

from app.core.config import SPEAKING_WORDS_PER_MINUTE
from app.schemas.script import ScriptRequest, ScriptResponse
from app.services.gemini_service import generate_content
from app.services.prompt_service import create_script_prompt

router = APIRouter()

@router.post("/api/generate-script", response_model=ScriptResponse)
def generate_script(data: ScriptRequest):

    prompt = create_script_prompt(
        data,
        data.selected_title,
        data.selected_hook,
        data.outline
    )

    try:
        response = generate_content(prompt)
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to generate the script right now. Please try again later."
        )

    if not response.strip():
        raise HTTPException(
            status_code=503,
            detail="Gemini returned an empty response. Please try again later."
        )

    word_count = len(response.split())

    estimated_duration = round(word_count / SPEAKING_WORDS_PER_MINUTE, 2)

    return {
        "script": response,
        "word_count": word_count,
        "estimated_duration": estimated_duration
    }