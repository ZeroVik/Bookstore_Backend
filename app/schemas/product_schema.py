from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    type: str
    author: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_path: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True
