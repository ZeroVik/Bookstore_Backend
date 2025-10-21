from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.book import Book
from app.schemas.ai_schema import AIRequest
import requests

router = APIRouter(prefix="/ai", tags=["AI"])


def ask_llama(prompt: str) -> str:
    """
    Ask the local Ollama model via HTTP API (fast and local).
    """
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3:latest",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip() or "No response from AI."

    except requests.exceptions.Timeout:
        return "Sorry, the AI took too long to respond."
    except requests.exceptions.ConnectionError:
        return "Could not connect to Ollama. Please ensure 'ollama serve' is running."
    except Exception as e:
        return f"Unexpected error: {e}"


@router.post("/recommend")
async def recommend_book(request: AIRequest, db: AsyncSession = Depends(get_db)):
    """
    Recommend only books that exist in the database,
    but sound natural and conversational.
    """
    query = request.query.lower()

    # Fetch all books
    result = await db.execute(select(Book))
    books = result.scalars().all()

    if not books:
        return {"recommendation": "No books found in the database."}

    # Build book list for the prompt
    book_list = [
        f"{book.title} by {book.author} (Genre: {book.genre})"
        for book in books if book.title and book.author
    ]

    # Refined prompt: natural tone + strict rule
    prompt = (
        f"You are a friendly book advisor. You help users find books from our store.\n\n"
        f"Here’s the list of ALL books available in the store (you CANNOT use anything else):\n"
        f"{chr(10).join(book_list)}\n\n"
        f"The user said: '{query}'\n\n"
        f"Your job:\n"
        f"- Pick one or more books ONLY from the list above.\n"
        f"- Never invent books or mention authors not listed.\n"
        f"- Speak like a human — friendly, short, and personal (2–3 sentences max).\n"
        f"- If nothing fits, say: 'Sorry, I couldn’t find anything that matches your taste right now.'\n\n"
        f"Now reply in a warm, natural way."
    )

    ai_response = ask_llama(prompt)
    return {"recommendation": ai_response}
