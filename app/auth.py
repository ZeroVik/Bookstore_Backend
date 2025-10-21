from fastapi import Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User

# Simple session-based dependency example
# (In production you'd use OAuth2 or JWT, but this works for now)

async def get_current_user(username: str | None = None, db: AsyncSession = Depends(get_db)):
    """
    Retrieve the current user from the database by username.
    """
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


async def admin_required(current_user: User = Depends(get_current_user)):
    """
    Allow access only if the current user has the 'admin' role.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user
