from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.category import Category  # ✅ This is the MODEL
from app.schemas.category_schema import CategoryCreate  # ✅ This is the SCHEMA
from app.auth import admin_required

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", dependencies=[Depends(admin_required)])
async def add_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Category).where(Category.name == category.name))
    result = existing.scalars().first()
    if result:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = Category(name=category.name, description=category.description)
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category
