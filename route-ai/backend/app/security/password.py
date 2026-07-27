import bcrypt
from passlib.context import CryptContext

# Passlib 1.7.4 compatibility patch for bcrypt >= 4.0 / 5.0
try:
    if not hasattr(bcrypt, "__about__"):
        bcrypt.__about__ = type("about", (), {"__version__": getattr(bcrypt, "__version__", "4.0.0")})()
    _orig_hashpw = bcrypt.hashpw

    def _safe_hashpw(password: bytes, salt: bytes) -> bytes:
        return _orig_hashpw(password[:72], salt)

    bcrypt.hashpw = _safe_hashpw
except Exception:
    pass

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain text password using bcrypt via passlib.

    Args:
        password: The plain text password string.

    Returns:
        The hashed password string suitable for database storage.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a stored hashed password.

    Args:
        plain_password: The user-provided plain text password.
        hashed_password: The stored bcrypt hashed password.

    Returns:
        True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Alias for ``hash_password`` for backward compatibility."""
    return hash_password(password)


