import os, shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.core.security import admin_required
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "public/uploads/books")

@router.post("/book-image", dependencies=[Depends(admin_required)])
async def upload_book_image(file: UploadFile = File(...)):
    """
    Admin can upload a book cover image file.
    Returns the relative URL for database storage.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Generate a public URL (to be stored in DB)
    public_url = f"/{UPLOAD_DIR}/{file.filename}"
    return {"image_url": public_url}
