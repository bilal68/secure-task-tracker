# app/api/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.db.models import User
from app.schemas.auth import TokenOut
from app.schemas.user import UserOut, RegisterIn
from app.crud import user_crud
from app.api.dependencies import get_current_user
from app.db.models import User

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    # Check if user already exists
    if user_crud.get_user_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Create and return new user
    user = user_crud.create_user(db, payload)
    return user


@router.post("/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2 form uses "username" for the identifier; we treat it as email
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    token = create_access_token(
        subject=user.email, user_id=int(user.id), role=str(user.role)
    )
    return TokenOut(access_token=token)


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
