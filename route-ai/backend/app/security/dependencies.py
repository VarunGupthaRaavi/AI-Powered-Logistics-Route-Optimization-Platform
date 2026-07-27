"""Authentication and authorization FastAPI dependencies."""

from typing import Callable, Sequence

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.database.session import get_db
from app.models.user import User
from app.repositories.user_repository import user_repository
from app.security.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """FastAPI dependency to extract JWT Bearer token and return current authenticated user.

    Args:
        db: Database session injected via dependency.
        token: JWT bearer token extracted from HTTP Authorization header.

    Returns:
        User model instance if valid and active.

    Raises:
        HTTPException: 401 Unauthorized if token missing, invalid, or user inactive.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate authentication credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        sub: str = payload.get("sub")
        if not sub:
            raise credentials_exception
        user_id = int(sub)
    except (JWTError, ValueError):
        raise credentials_exception

    user = user_repository.get_by_id(db, user_id=user_id)
    if not user:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def require_role(*allowed_roles: str) -> Callable[[User], User]:
    """Dependency factory enforcing Role-Based Access Control (RBAC).

    Args:
        *allowed_roles: Names of roles permitted to access the endpoint (e.g. "Admin", "User").

    Returns:
        A FastAPI dependency callable validating user role.
    """

    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        user_role = current_user.role.role_name if current_user.role else None
        if not user_role or user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied. Required role: {', '.join(allowed_roles)}.",
            )
        return current_user

    return role_checker
