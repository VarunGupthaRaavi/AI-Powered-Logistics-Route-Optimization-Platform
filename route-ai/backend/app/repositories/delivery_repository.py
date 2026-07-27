"""DeliveryRepository for delivery entity database operations.

Contains pure database access queries using SQLAlchemy 2.0 syntax.
"""

from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.delivery import Delivery


class DeliveryRepository:
    """Repository handling database access for Delivery records."""

    def __init__(self, db: Optional[Session] = None) -> None:
        self.db = db

    def get_by_id(self, db: Session, delivery_id: int) -> Optional[Delivery]:
        """Fetch a single delivery by primary key delivery_id.

        Args:
            db: Database session.
            delivery_id: Primary key integer.

        Returns:
            Delivery model instance if found, None otherwise.
        """
        stmt = select(Delivery).where(Delivery.delivery_id == delivery_id)
        return db.scalar(stmt)

    def list_deliveries(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        customer_id: Optional[int] = None,
    ) -> tuple[list[Delivery], int]:
        """Fetch paginated deliveries with optional status and customer filters.

        Args:
            db: Database session.
            skip: Number of records to offset/skip.
            limit: Maximum records to return.
            status: Optional delivery_status string filter.
            customer_id: Optional customer_id integer filter.

        Returns:
            Tuple of (list of matching Delivery records, total matching count).
        """
        stmt = select(Delivery)
        count_stmt = select(func.count()).select_from(Delivery)

        if status:
            stmt = stmt.where(Delivery.delivery_status == status)
            count_stmt = count_stmt.where(Delivery.delivery_status == status)

        if customer_id:
            stmt = stmt.where(Delivery.customer_id == customer_id)
            count_stmt = count_stmt.where(Delivery.customer_id == customer_id)

        total = db.scalar(count_stmt) or 0
        stmt = stmt.order_by(Delivery.created_at.desc()).offset(skip).limit(limit)
        items = list(db.scalars(stmt).all())

        return items, total

    def create_delivery(self, db: Session, delivery_data: dict) -> Delivery:
        """Create and persist a new Delivery record.

        Args:
            db: Database session.
            delivery_data: Dictionary of delivery fields.

        Returns:
            Created Delivery model instance.
        """
        delivery = Delivery(**delivery_data)
        db.add(delivery)
        db.commit()
        db.refresh(delivery)
        return delivery

    def update_delivery(self, db: Session, delivery: Delivery, update_data: dict) -> Delivery:
        """Update fields on an existing Delivery record.

        Args:
            db: Database session.
            delivery: Existing Delivery model instance.
            update_data: Dictionary of field names and new values.

        Returns:
            Updated Delivery model instance.
        """
        for key, value in update_data.items():
            if value is not None and hasattr(delivery, key):
                setattr(delivery, key, value)

        db.add(delivery)
        db.commit()
        db.refresh(delivery)
        return delivery

    def delete_delivery(self, db: Session, delivery: Delivery) -> bool:
        """Delete a Delivery record from the database.

        Args:
            db: Database session.
            delivery: Delivery instance to remove.

        Returns:
            True if deletion succeeded.
        """
        db.delete(delivery)
        db.commit()
        return True


delivery_repository = DeliveryRepository()
