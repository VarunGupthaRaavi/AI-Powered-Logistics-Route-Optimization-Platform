from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.delivery import Delivery
    from app.models.route import Route


class RouteStop(Base):
    __tablename__ = "route_stops"
    __table_args__ = (
        UniqueConstraint("route_id", "stop_sequence", name="uq_route_stops_route_sequence"),
        UniqueConstraint("route_id", "delivery_id", name="uq_route_stops_route_delivery"),
    )

    stop_id: Mapped[int] = mapped_column(primary_key=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.route_id"), index=True)
    delivery_id: Mapped[int] = mapped_column(ForeignKey("deliveries.delivery_id"), index=True)
    stop_sequence: Mapped[int] = mapped_column(Integer)
    eta: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    stop_status: Mapped[str] = mapped_column(String(50), default="pending", server_default="pending")

    route: Mapped[Route] = relationship(back_populates="stops")
    delivery: Mapped[Delivery] = relationship(back_populates="route_stops")
