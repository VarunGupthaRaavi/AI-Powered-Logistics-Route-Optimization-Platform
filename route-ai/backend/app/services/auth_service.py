"""AuthService encapsulating core authentication business logic."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import user_repository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.security.jwt import create_access_token
from app.security.password import hash_password, verify_password


class AuthService:
    """Service handling user registration, authentication, and token issuance."""

    DEFAULT_ROLE_NAME = "User"

    def register_user(self, db: Session, register_data: RegisterRequest) -> UserResponse:
        """Register a new user after checking email uniqueness and hashing password.

        Args:
            db: Database session.
            register_data: Registration payload with email, password, full_name, etc.

        Returns:
            UserResponse schema with user details and assigned role.

        Raises:
            HTTPException: 400 Bad Request if email already registered.
        """
        if user_repository.email_exists(db, register_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email address already exists.",
            )

        # Get or seed default "User" role
        role = user_repository.get_role_by_name(db, self.DEFAULT_ROLE_NAME)
        if not role:
            role = user_repository.create_role(db, self.DEFAULT_ROLE_NAME)

        hashed_pwd = hash_password(register_data.password)

        user = user_repository.create_user(
            db,
            email=register_data.email,
            password_hash=hashed_pwd,
            full_name=register_data.full_name,
            role_id=role.role_id,
            phone=register_data.phone,
            is_active=True,
        )

        return UserResponse(
            user_id=user.user_id,
            email=user.email,
            full_name=user.full_name,
            phone=user.phone,
            is_active=user.is_active,
            role_id=role.role_id,
            role_name=role.role_name,
            created_at=user.created_at,
        )

    def authenticate_user(self, db: Session, login_data: LoginRequest) -> TokenResponse:
        """Authenticate user credentials and issue JWT access token.

        Args:
            db: Database session.
            login_data: Login credentials (email, password).

        Returns:
            TokenResponse containing encoded access token and user profile.

        Raises:
            HTTPException: 401 Unauthorized if authentication fails.
        """
        user = user_repository.get_by_email(db, login_data.email)
        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is inactive.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        role_name = user.role.role_name if user.role else self.DEFAULT_ROLE_NAME

        token_data = {
            "sub": str(user.user_id),
            "email": user.email,
            "role": role_name,
        }
        access_token = create_access_token(token_data)

        user_response = UserResponse(
            user_id=user.user_id,
            email=user.email,
            full_name=user.full_name,
            phone=user.phone,
            is_active=user.is_active,
            role_id=user.role_id,
            role_name=role_name,
            created_at=user.created_at,
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response,
        )

    def get_current_user_profile(self, user: User) -> UserResponse:
        """Format an authenticated User model instance into UserResponse.

        Args:
            user: Authenticated User model instance.

        Returns:
            Formatted UserResponse.
        """
        return UserResponse(
            user_id=user.user_id,
            email=user.email,
            full_name=user.full_name,
            phone=user.phone,
            is_active=user.is_active,
            role_id=user.role_id,
            role_name=user.role.role_name if user.role else None,
            created_at=user.created_at,
        )


auth_service = AuthService()
