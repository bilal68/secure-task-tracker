# app/crud/user_crud.py

from sqlalchemy.orm import Session
from app.db.models import User, RoleEnum
from app.schemas.user import RegisterIn
from app.core.security import get_password_hash


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_in: RegisterIn) -> User:
    hashed_password = get_password_hash(user_in.password)
    user = User(
        email=user_in.email,
        password_hash=hashed_password,
        role=RoleEnum.user
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
