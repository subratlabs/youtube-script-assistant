from google import genai

from app.core.config import GEMINI_API_KEY, GEMINI_MODEL


client = genai.Client(api_key=GEMINI_API_KEY)


def generate_content(prompt: str, json_mode: bool = False):

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            } if json_mode else None
        )

        return response.text

    except Exception as e:
        print(f"Gemini API error: {type(e).__name__}: {e}")
        raise Exception("Gemini API request failed") from e