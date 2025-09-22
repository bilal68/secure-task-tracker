from datetime import datetime, timedelta, timezone
import email
from typing import Any, Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(
    subject: str, *, role: str, user_id: int, expires_minutes: Optional[int] = None
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.access_token_expire_minutes
    )
    to_encode: dict[str, Any] = {
        "sub": subject,
        "role": role,
        "user_id": user_id,
        "exp": expire,
    }
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict[str, Any]:
    # Will raise JWTError if invalid/expired
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
