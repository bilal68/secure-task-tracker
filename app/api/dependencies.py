# app/api/dependencies.py
from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import SessionLocal
from app.db.models import User
from app.core.security import decode_token
from app.core.config import oauth2_scheme
from app.crud.user_crud import get_user_by_id

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = decode_token(token)
        user_id: int | None = payload.get("user_id")
        if not user_id:
            raise ValueError("missing sub")
    except Exception as e:
        print("DEBUG error:", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if str(current_user.role) != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return current_user
