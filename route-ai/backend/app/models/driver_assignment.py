from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.delivery import Delivery
    from app.models.driver import Driver


class DriverAssignment(Base):
    __tablename__ = "driver_assignments"

    assignment_id: Mapped[int] = mapped_column(primary_key=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.driver_id"), index=True)
    delivery_id: Mapped[int] = mapped_column(ForeignKey("deliveries.delivery_id"), index=True)
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    assignment_status: Mapped[str] = mapped_column(
        String(50), default="assigned", server_default="assigned", index=True
    )

    driver: Mapped[Driver] = relationship(back_populates="assignments")
    delivery: Mapped[Delivery] = relationship(back_populates="assignments")
