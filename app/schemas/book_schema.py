from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    genre: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = None
    stock: Optional[int] = 0
    image_url: Optional[str] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    class Config:
        orm_mode = True
