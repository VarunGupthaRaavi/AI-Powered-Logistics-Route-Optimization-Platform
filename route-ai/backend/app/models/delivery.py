from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.agent_task import AgentTask
    from app.models.customer import Customer
    from app.models.delivery_schedule import DeliverySchedule
    from app.models.driver import Driver
    from app.models.driver_assignment import DriverAssignment
    from app.models.eta_prediction import ETAPrediction
    from app.models.route_stop import RouteStop
    from app.models.vehicle import Vehicle


class Delivery(Base):
    __tablename__ = "deliveries"
    __table_args__ = (Index("ix_deliveries_status_created_at", "delivery_status", "created_at"),)

    delivery_id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.customer_id"), index=True)
    vehicle_id: Mapped[int | None] = mapped_column(
        ForeignKey("vehicles.vehicle_id"), nullable=True, index=True
    )
    driver_id: Mapped[int | None] = mapped_column(
        ForeignKey("drivers.driver_id"), nullable=True, index=True
    )
    pickup_location: Mapped[str] = mapped_column(String(500))
    drop_location: Mapped[str] = mapped_column(String(500))
    package_weight: Mapped[float] = mapped_column(Float)
    priority: Mapped[str] = mapped_column(String(50), default="normal", server_default="normal")
    delivery_window_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    delivery_window_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    delivery_status: Mapped[str] = mapped_column(
        String(50), default="pending", server_default="pending", index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    customer: Mapped[Customer] = relationship(back_populates="deliveries")
    vehicle: Mapped[Vehicle | None] = relationship(back_populates="deliveries")
    driver: Mapped[Driver | None] = relationship(back_populates="deliveries")
    route_stops: Mapped[list[RouteStop]] = relationship(back_populates="delivery")
    eta_predictions: Mapped[list[ETAPrediction]] = relationship(back_populates="delivery")
    schedules: Mapped[list[DeliverySchedule]] = relationship(back_populates="delivery")
    assignments: Mapped[list[DriverAssignment]] = relationship(back_populates="delivery")
    agent_tasks: Mapped[list[AgentTask]] = relationship(back_populates="delivery")
