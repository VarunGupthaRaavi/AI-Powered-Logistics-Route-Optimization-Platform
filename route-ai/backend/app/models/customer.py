from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.delivery import Delivery


class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(primary_key=True)
    company_name: Mapped[str] = mapped_column(String(255), index=True)
    contact_name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    address: Mapped[str] = mapped_column(String(500))

    deliveries: Mapped[list[Delivery]] = relationship(back_populates="customer")
