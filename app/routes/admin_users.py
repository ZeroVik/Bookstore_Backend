from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.user import User
from app.core.security import admin_required

router = APIRouter(prefix="/admin/users", tags=["Admin - Users"])

@router.get("/", dependencies=[Depends(admin_required)])
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [{"id": u.id, "username": u.username, "role": u.role} for u in users]

@router.delete("/{user_id}", dependencies=[Depends(admin_required)])
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role == "admin":
        raise HTTPException(status_code=403, detail="Cannot delete other admins")

    await db.delete(user)
    await db.commit()
    return {"message": f"User {user.username} deleted successfully"}
