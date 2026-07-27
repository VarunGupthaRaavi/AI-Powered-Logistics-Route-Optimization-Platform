"""UserRepository for user entity database operations.

Contains only database access methods using SQLAlchemy 2.0 style queries.
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.role import Role
from app.models.user import User


class UserRepository:
    """Repository handling database operations for User and Role entities."""

    def __init__(self, db: Optional[Session] = None) -> None:
        self.db = db

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Fetch a single user by email address with loaded role.

        Args:
            db: Database session.
            email: Email address to search for.

        Returns:
            User model instance if found, None otherwise.
        """
        stmt = select(User).options(joinedload(User.role)).where(User.email == email)
        return db.scalar(stmt)

    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """Fetch a single user by primary key user_id with loaded role.

        Args:
            db: Database session.
            user_id: User ID integer.

        Returns:
            User model instance if found, None otherwise.
        """
        stmt = select(User).options(joinedload(User.role)).where(User.user_id == user_id)
        return db.scalar(stmt)

    def email_exists(self, db: Session, email: str) -> bool:
        """Check if an email address is already registered.

        Args:
            db: Database session.
            email: Email address to check.

        Returns:
            True if email exists in database, False otherwise.
        """
        stmt = select(User.user_id).where(User.email == email)
        return db.scalar(stmt) is not None

    def create_user(
        self,
        db: Session,
        *,
        email: str,
        password_hash: str,
        full_name: str,
        role_id: int,
        phone: Optional[str] = None,
        is_active: bool = True,
    ) -> User:
        """Create and persist a new User record.

        Args:
            db: Database session.
            email: User's unique email.
            password_hash: Hashed password string.
            full_name: User's full name.
            role_id: Assigned Role ID foreign key.
            phone: Optional phone number.
            is_active: User active state flag.

        Returns:
            The created User instance.
        """
        user = User(
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            role_id=role_id,
            phone=phone,
            is_active=is_active,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_role_by_name(self, db: Session, role_name: str) -> Optional[Role]:
        """Fetch a role record by name.

        Args:
            db: Database session.
            role_name: Name of role (e.g. "Admin", "User").

        Returns:
            Role model instance if found, None otherwise.
        """
        stmt = select(Role).where(Role.role_name == role_name)
        return db.scalar(stmt)

    def create_role(self, db: Session, role_name: str) -> Role:
        """Create and persist a new Role record.

        Args:
            db: Database session.
            role_name: Unique role name.

        Returns:
            Created Role instance.
        """
        role = Role(role_name=role_name)
        db.add(role)
        db.commit()
        db.refresh(role)
        return role


user_repository = UserRepository()
