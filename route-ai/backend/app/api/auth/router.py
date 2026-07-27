"""Authentication API endpoints for registration, login, and user profile."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.security.dependencies import get_current_user
from app.services.auth_service import auth_service

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user account",
    description="Validates registration request, ensures email is unique, hashes password, assigns default User role, and persists new user.",
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
) -> UserResponse:
    """Register a new user in the platform."""
    return auth_service.register_user(db, request)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user and obtain JWT token",
    description="Verifies user credentials against stored bcrypt password hash and returns a signed JWT access token.",
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Authenticate user credentials and issue access token."""
    return auth_service.authenticate_user(db, request)


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get authenticated user profile",
    description="Protected endpoint returning profile details of the currently authenticated user based on JWT Bearer token.",
)
def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Return profile details of currently authenticated user."""
    return auth_service.get_current_user_profile(current_user)
