from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.route import Route


class RouteAdjustment(Base):
    __tablename__ = "route_adjustments"

    adjustment_id: Mapped[int] = mapped_column(primary_key=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.route_id"), index=True)
    reason: Mapped[str] = mapped_column(String(500))
    updated_route: Mapped[str] = mapped_column(Text)
    adjusted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    route: Mapped[Route] = relationship(back_populates="adjustments")
