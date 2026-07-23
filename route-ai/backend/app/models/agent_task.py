from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.ai_agent import AIAgent
    from app.models.delivery import Delivery


class AgentTask(Base):
    __tablename__ = "agent_tasks"

    task_id: Mapped[int] = mapped_column(primary_key=True)
    agent_id: Mapped[int] = mapped_column(ForeignKey("ai_agents.agent_id"), index=True)
    delivery_id: Mapped[int] = mapped_column(ForeignKey("deliveries.delivery_id"), index=True)
    task_result: Mapped[str | None] = mapped_column(Text, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    agent: Mapped[AIAgent] = relationship(back_populates="tasks")
    delivery: Mapped[Delivery] = relationship(back_populates="agent_tasks")
