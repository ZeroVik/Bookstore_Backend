from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from fastapi.security import HTTPBearer
import os

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
auth_scheme = HTTPBearer()

def get_current_user(token: str = Depends(auth_scheme)):
    credentials = token.credentials
    try:
        payload = jwt.decode(credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def admin_required(current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return current_user
