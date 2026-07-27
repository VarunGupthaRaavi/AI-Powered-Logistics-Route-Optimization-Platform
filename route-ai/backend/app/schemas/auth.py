"""Authentication Pydantic schemas for request validation and response serialization."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    """Payload schema for user registration."""

    email: EmailStr = Field(..., description="User's unique email address")
    password: str = Field(..., min_length=8, description="User's password (min 8 characters)")
    full_name: str = Field(..., min_length=1, max_length=255, description="User's full name")
    phone: Optional[str] = Field(None, max_length=30, description="Optional phone number")


class LoginRequest(BaseModel):
    """Payload schema for user login authentication."""

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's account password")


class UserResponse(BaseModel):
    """Response schema representing a User profile."""

    model_config = ConfigDict(from_attributes=True)

    user_id: int = Field(..., description="Unique User ID")
    email: EmailStr = Field(..., description="User email address")
    full_name: str = Field(..., description="User full name")
    phone: Optional[str] = Field(None, description="User phone number")
    is_active: bool = Field(True, description="Account status flag")
    role_id: int = Field(..., description="Role ID foreign key")
    role_name: Optional[str] = Field(None, description="Name of the assigned role")
    created_at: datetime = Field(..., description="Timestamp when account was created")


class TokenResponse(BaseModel):
    """Response schema containing JWT access token."""

    access_token: str = Field(..., description="Encoded JWT access token")
    token_type: str = Field("bearer", description="Token type designation")
    user: Optional[UserResponse] = Field(None, description="Authenticated user profile details")
