from sqlalchemy import Column, Integer, String, Float, Text
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False, default="book")  # book, magazine, etc.
    author = Column(String(255), nullable=True)                # optional
    genre = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    image_path = Column(String(255), nullable=True)
