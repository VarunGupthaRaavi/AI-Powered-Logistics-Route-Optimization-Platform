from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.document_embedding import DocumentEmbedding


class Document(Base):
    __tablename__ = "documents"

    document_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500), index=True)
    category: Mapped[str] = mapped_column(String(100), index=True)
    file_path: Mapped[str] = mapped_column(String(1_000), unique=True)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    embeddings: Mapped[list[DocumentEmbedding]] = relationship(
        back_populates="document", cascade="all, delete-orphan"
    )
