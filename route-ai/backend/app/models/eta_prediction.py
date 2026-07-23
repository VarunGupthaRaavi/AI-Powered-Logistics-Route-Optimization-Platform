from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.delivery import Delivery


class ETAPrediction(Base):
    __tablename__ = "eta_predictions"

    prediction_id: Mapped[int] = mapped_column(primary_key=True)
    delivery_id: Mapped[int] = mapped_column(ForeignKey("deliveries.delivery_id"), index=True)
    predicted_eta: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    confidence_score: Mapped[float] = mapped_column(Float)
    model_name: Mapped[str] = mapped_column(String(255))
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    delivery: Mapped[Delivery] = relationship(back_populates="eta_predictions")
