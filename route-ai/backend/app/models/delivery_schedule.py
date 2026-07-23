from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.delivery import Delivery


class DeliverySchedule(Base):
    __tablename__ = "delivery_schedules"

    schedule_id: Mapped[int] = mapped_column(primary_key=True)
    delivery_id: Mapped[int] = mapped_column(ForeignKey("deliveries.delivery_id"), index=True)
    scheduled_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    scheduled_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    schedule_status: Mapped[str] = mapped_column(
        String(50), default="scheduled", server_default="scheduled"
    )

    delivery: Mapped[Delivery] = relationship(back_populates="schedules")
