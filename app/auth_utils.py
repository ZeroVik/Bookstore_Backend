from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os

# Adjust this secret to match your login logic
SECRET_KEY = os.getenv("JWT_SECRET", "45d7c61caf7c150435b90a252d6d761b1765f668b37602e646994144fddfb69ccad164d7a78acbd1b283a0cc2c4cdf4c8a826c3a7a262eb0f2194fcb9f9f9211")
ALGORITHM = "HS256"

security = HTTPBearer()


def decode_token(token: str):
    """
    Decode a JWT token and return its payload.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def admin_required(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency used to protect admin routes.
    Ensures the current user has role = 'admin'.
    """
    token = credentials.credentials
    payload = decode_token(token)
    role = payload.get("role")

    if role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    return payload
