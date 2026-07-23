from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.route import Route


class RouteOptimization(Base):
    __tablename__ = "route_optimizations"

    optimization_id: Mapped[int] = mapped_column(primary_key=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.route_id"), index=True)
    fuel_saved: Mapped[float] = mapped_column(Float)
    distance_saved: Mapped[float] = mapped_column(Float)
    time_saved: Mapped[float] = mapped_column(Float)
    optimized_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    route: Mapped[Route] = relationship(back_populates="optimizations")
