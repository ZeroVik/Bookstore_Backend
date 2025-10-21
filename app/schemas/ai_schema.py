from pydantic import BaseModel

class AIRequest(BaseModel):
    query: str
