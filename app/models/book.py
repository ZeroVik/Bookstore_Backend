from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    description = Column(Text)
    genre = Column(String(100))

    # ✅ THIS IS THE IMPORTANT LINE:
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)

    price = Column(Float)
    stock = Column(Integer, default=0)
    image_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ✅ Relationship (now works because of the ForeignKey)
    category = relationship("Category", backref="books")
