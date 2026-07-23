from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config.settings import settings
from app.database.base import Base


engine: Engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=1_800,
    pool_timeout=30,
)
SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """Yield one database session per request and always close it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


__all__ = ["Base", "SessionLocal", "engine", "get_db"]
