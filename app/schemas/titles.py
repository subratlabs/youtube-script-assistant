from pydantic import BaseModel

class TitlesResponse(BaseModel):
    titles: list[str]