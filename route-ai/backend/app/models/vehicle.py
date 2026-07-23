from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.delivery import Delivery
    from app.models.driver import Driver


class Vehicle(Base):
    __tablename__ = "vehicles"

    vehicle_id: Mapped[int] = mapped_column(primary_key=True)
    driver_id: Mapped[int | None] = mapped_column(
        ForeignKey("drivers.driver_id"), nullable=True, index=True
    )
    vehicle_number: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    vehicle_type: Mapped[str] = mapped_column(String(100))
    capacity: Mapped[int] = mapped_column(Integer)
    fuel_type: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50), default="available", server_default="available")

    driver: Mapped[Driver | None] = relationship(back_populates="vehicles")
    deliveries: Mapped[list[Delivery]] = relationship(back_populates="vehicle")
