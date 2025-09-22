# app/schemas/user.py

from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict


# Input schema for user registration (e.g. /register)
class RegisterIn(BaseModel):
    email: EmailStr
    password: str


# Output schema used in API response (hides password)
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Required for Pydantic v2
    id: int
    email: EmailStr
    role: str
