from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.delivery import Delivery
    from app.models.driver_assignment import DriverAssignment
    from app.models.route import Route
    from app.models.user import User
    from app.models.vehicle import Vehicle


class Driver(Base):
    __tablename__ = "drivers"

    driver_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), unique=True, index=True)
    license_number: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(50), default="available", server_default="available")
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped[User] = relationship(back_populates="driver")
    vehicles: Mapped[list[Vehicle]] = relationship(back_populates="driver")
    deliveries: Mapped[list[Delivery]] = relationship(back_populates="driver")
    routes: Mapped[list[Route]] = relationship(back_populates="driver")
    assignments: Mapped[list[DriverAssignment]] = relationship(back_populates="driver")
