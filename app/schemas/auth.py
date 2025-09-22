# app/schemas/auth.py
from pydantic import BaseModel, EmailStr


# OAuth2PasswordRequestForm sends "username" for the identifier (we’ll treat it as email)
class LoginIn(BaseModel):
    username: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
