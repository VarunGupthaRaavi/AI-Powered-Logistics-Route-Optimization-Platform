"""RouteAI SQLAlchemy models.

Importing this package registers every model with ``Base.metadata`` for Alembic.
"""

from app.database.base import Base
from app.models.agent_task import AgentTask
from app.models.ai_agent import AIAgent
from app.models.audit_log import AuditLog
from app.models.customer import Customer
from app.models.delivery import Delivery
from app.models.delivery_schedule import DeliverySchedule
from app.models.document import Document
from app.models.document_embedding import DocumentEmbedding
from app.models.driver import Driver
from app.models.driver_assignment import DriverAssignment
from app.models.eta_prediction import ETAPrediction
from app.models.notification import Notification
from app.models.role import Role
from app.models.route import Route
from app.models.route_adjustment import RouteAdjustment
from app.models.route_optimization import RouteOptimization
from app.models.route_stop import RouteStop
from app.models.traffic_data import TrafficData
from app.models.user import User
from app.models.vehicle import Vehicle

__all__ = [
    "AIAgent",
    "AgentTask",
    "AuditLog",
    "Base",
    "Customer",
    "Delivery",
    "DeliverySchedule",
    "Document",
    "DocumentEmbedding",
    "Driver",
    "DriverAssignment",
    "ETAPrediction",
    "Notification",
    "Role",
    "Route",
    "RouteAdjustment",
    "RouteOptimization",
    "RouteStop",
    "TrafficData",
    "User",
    "Vehicle",
]
