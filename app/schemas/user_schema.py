from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    full_name: str
    username: str
    password: str
    role_id: int


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[int] = None


class UserResponse(BaseModel):
    user_id: int
    full_name: str
    username: str
    role_id: int
    created_at: datetime

    class Config:
        from_attributes = True
