from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.agent_task import AgentTask


class AIAgent(Base):
    __tablename__ = "ai_agents"

    agent_id: Mapped[int] = mapped_column(primary_key=True)
    agent_name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    responsibility: Mapped[str] = mapped_column(String(500))

    tasks: Mapped[list[AgentTask]] = relationship(
        back_populates="agent", cascade="all, delete-orphan"
    )
