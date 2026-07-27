from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from app.schemas.auth import RegisterRequest, UserResponse


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(RegisterRequest):
    pass


__all__ = ["UserBase", "UserCreate", "UserResponse", "RegisterRequest"]

