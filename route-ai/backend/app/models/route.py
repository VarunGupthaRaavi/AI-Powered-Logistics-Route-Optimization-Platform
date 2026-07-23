from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.driver import Driver
    from app.models.route_adjustment import RouteAdjustment
    from app.models.route_optimization import RouteOptimization
    from app.models.route_stop import RouteStop
    from app.models.traffic_data import TrafficData


class Route(Base):
    __tablename__ = "routes"

    route_id: Mapped[int] = mapped_column(primary_key=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.driver_id"), index=True)
    total_distance: Mapped[float] = mapped_column(Float)
    estimated_duration: Mapped[float] = mapped_column(Float)
    estimated_cost: Mapped[float] = mapped_column(Float)
    optimized: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    driver: Mapped[Driver] = relationship(back_populates="routes")
    stops: Mapped[list[RouteStop]] = relationship(
        back_populates="route", cascade="all, delete-orphan", order_by="RouteStop.stop_sequence"
    )
    traffic_data: Mapped[list[TrafficData]] = relationship(
        back_populates="route", cascade="all, delete-orphan"
    )
    optimizations: Mapped[list[RouteOptimization]] = relationship(
        back_populates="route", cascade="all, delete-orphan"
    )
    adjustments: Mapped[list[RouteAdjustment]] = relationship(
        back_populates="route", cascade="all, delete-orphan"
    )
