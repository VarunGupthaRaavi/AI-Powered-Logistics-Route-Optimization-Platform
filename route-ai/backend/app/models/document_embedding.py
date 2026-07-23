from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.document import Document


class DocumentEmbedding(Base):
    __tablename__ = "document_embeddings"

    embedding_id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.document_id"), index=True)
    vector_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    document: Mapped[Document] = relationship(back_populates="embeddings")
