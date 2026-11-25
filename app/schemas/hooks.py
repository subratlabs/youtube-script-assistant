from pydantic import BaseModel

class HooksResponse(BaseModel):
    hooks: list[str]