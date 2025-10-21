from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    description: str | None = None

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2
