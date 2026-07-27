"""DeliveryRepository for delivery entity database operations.

Contains pure database access queries using SQLAlchemy 2.0 syntax.
"""

from typing import Optional

from sqlalchemy import asc, desc, func, or_, select
from sqlalchemy.orm import Session

from app.models.delivery import Delivery


class DeliveryRepository:
    """Repository handling database access for Delivery records."""

    def __init__(self, db: Optional[Session] = None) -> None:
        self.db = db

    def get_by_id(self, db: Session, delivery_id: int) -> Optional[Delivery]:
        """Fetch a single delivery by primary key delivery_id."""
        stmt = select(Delivery).where(Delivery.delivery_id == delivery_id)
        return db.scalar(stmt)

    def list_deliveries(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        customer_id: Optional[int] = None,
        search: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[Delivery], int]:
        """Fetch paginated deliveries with search, status/priority filters, and dynamic sorting.

        Args:
            db: Database session.
            skip: Number of records to offset/skip.
            limit: Maximum records to return per page.
            status: Optional delivery_status filter (case-insensitive).
            priority: Optional priority filter (case-insensitive).
            customer_id: Optional customer_id integer filter.
            search: Optional search term matching pickup or drop locations.
            sort_by: Field name to sort by (created_at, package_weight, priority, delivery_id).
            sort_order: Sort direction ('asc' or 'desc').

        Returns:
            Tuple of (list of matching Delivery records, total matching count).
        """
        stmt = select(Delivery)
        count_stmt = select(func.count()).select_from(Delivery)

        # 1. Apply status filter (case-insensitive)
        if status:
            stmt = stmt.where(func.lower(Delivery.delivery_status) == status.lower())
            count_stmt = count_stmt.where(func.lower(Delivery.delivery_status) == status.lower())

        # 2. Apply priority filter (case-insensitive)
        if priority:
            stmt = stmt.where(func.lower(Delivery.priority) == priority.lower())
            count_stmt = count_stmt.where(func.lower(Delivery.priority) == priority.lower())

        # 3. Apply customer_id filter
        if customer_id:
            stmt = stmt.where(Delivery.customer_id == customer_id)
            count_stmt = count_stmt.where(Delivery.customer_id == customer_id)

        # 4. Apply text search across pickup_location and drop_location
        if search:
            search_pattern = f"%{search}%"
            search_filter = or_(
                Delivery.pickup_location.ilike(search_pattern),
                Delivery.drop_location.ilike(search_pattern),
            )
            stmt = stmt.where(search_filter)
            count_stmt = count_stmt.where(search_filter)

        # Execute count query to get total matching records before pagination
        total = db.scalar(count_stmt) or 0

        # 5. Dynamic Sorting
        sort_fields = {
            "created_at": Delivery.created_at,
            "package_weight": Delivery.package_weight,
            "priority": Delivery.priority,
            "delivery_id": Delivery.delivery_id,
            "delivery_status": Delivery.delivery_status,
        }
        column = sort_fields.get(sort_by, Delivery.created_at)
        direction = asc(column) if sort_order.lower() == "asc" else desc(column)

        # Apply sorting, offset, and limit
        stmt = stmt.order_by(direction).offset(skip).limit(limit)
        items = list(db.scalars(stmt).all())

        return items, total

    def create_delivery(self, db: Session, delivery_data: dict) -> Delivery:
        """Create and persist a new Delivery record."""
        delivery = Delivery(**delivery_data)
        db.add(delivery)
        db.commit()
        db.refresh(delivery)
        return delivery

    def update_delivery(self, db: Session, delivery: Delivery, update_data: dict) -> Delivery:
        """Update fields on an existing Delivery record."""
        for key, value in update_data.items():
            if value is not None and hasattr(delivery, key):
                setattr(delivery, key, value)

        db.add(delivery)
        db.commit()
        db.refresh(delivery)
        return delivery

    def delete_delivery(self, db: Session, delivery: Delivery) -> bool:
        """Delete a Delivery record from the database."""
        db.delete(delivery)
        db.commit()
        return True


delivery_repository = DeliveryRepository()
