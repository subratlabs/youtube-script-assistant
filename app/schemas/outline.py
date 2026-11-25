from pydantic import BaseModel

class OutlineResponse(BaseModel):
    outline: list[str]