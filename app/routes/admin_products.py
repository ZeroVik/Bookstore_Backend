from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.product import Product
from app.schemas.product_schema import ProductCreate, ProductResponse
from app.auth_utils import admin_required  # assuming your admin auth logic is here
import shutil
import os

router = APIRouter(prefix="/admin/products", tags=["Admin - Products"])


UPLOAD_DIR = "uploads/products"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", dependencies=[Depends(admin_required)], response_model=ProductResponse)
async def add_product(
    name: str = Form(...),
    type: str = Form(...),
    author: str = Form(None),
    genre: str = Form(None),
    description: str = Form(None),
    price: float = Form(None),
    image: UploadFile = File(None),
    db: AsyncSession = Depends(get_db)
):
    image_path = None
    if image:
        file_path = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_path = file_path

    new_product = Product(
        name=name,
        type=type,
        author=author,
        genre=genre,
        description=description,
        price=price,
        image_path=image_path,
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


@router.get("/", dependencies=[Depends(admin_required)], response_model=list[ProductResponse])
async def list_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    return result.scalars().all()
