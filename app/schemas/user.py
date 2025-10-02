from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    date_of_birth: Optional[date] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None

class User(UserBase):
    id: int
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None