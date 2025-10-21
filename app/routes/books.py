from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.book import Book
from app.schemas.book_schema import BookCreate, Book as BookOut
from app.core.security import admin_required

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=list[BookOut])
async def list_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book))
    return result.scalars().all()

@router.post("/", response_model=BookOut, dependencies=[Depends(admin_required)])
async def add_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    new_book = Book(**book.dict())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book
