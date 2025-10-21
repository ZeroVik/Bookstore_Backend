from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.book import Book
from app.ai.llama_client import llama_chat
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["AI"])

# Response schema for docs
class AIResponse(BaseModel):
    answer: str

@router.post("/chat", response_model=AIResponse)
async def chat(prompt: str = Body(..., embed=True)):
    """
    Basic chat endpoint with LLaMA.
    """
    answer = await llama_chat(prompt)
    return {"answer": answer}

@router.post("/recommend", response_model=AIResponse)
async def recommend(
    keyword: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    """
    Recommend similar books based on the database and keyword/title.
    """
    # 1️⃣ Get all books from the DB
    result = await db.execute(select(Book))
    books = result.scalars().all()

    if not books:
        raise HTTPException(status_code=404, detail="No books found in the database.")

    # 2️⃣ Format books for AI
    book_list = "\n".join(
        [f"- {b.title} by {b.author}: {b.description or 'No description'}" for b in books]
    )

    # 3️⃣ Create the prompt for LLaMA
    prompt = f"""
You are an intelligent book recommendation AI.
Below is the list of available books in our store:

{book_list}

The user is interested in: "{keyword}"

From the above list, suggest 3 books that best match their interest.
Explain each recommendation briefly and naturally.
    """

    # 4️⃣ Ask LLaMA
    answer = await llama_chat(prompt)
    return {"answer": answer}
