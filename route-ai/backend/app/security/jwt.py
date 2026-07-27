from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from app.config.settings import settings


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    """Create a signed JWT access token containing payload claims.

    Args:
        data: Dictionary of claims to include in payload.
        expires_delta: Optional custom lifetime duration for token.

    Returns:
        Encoded JWT token string.
    """
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "iat": now})
    return jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT access token payload.

    Args:
        token: Encoded JWT token string.

    Returns:
        Decoded payload dictionary.

    Raises:
        JWTError: If token decoding or validation fails.
    """
    return jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )


def verify_access_token(token: str) -> dict[str, Any] | None:
    """Verify and decode JWT access token, returning payload or None if invalid.

    Args:
        token: Encoded JWT token string.

    Returns:
        Decoded payload dictionary if valid, None otherwise.
    """
    try:
        return decode_access_token(token)
    except JWTError:
        return None


def verify_token(token: str) -> dict[str, Any] | None:
    """Alias for ``verify_access_token`` for backward compatibility."""
    return verify_access_token(token)

