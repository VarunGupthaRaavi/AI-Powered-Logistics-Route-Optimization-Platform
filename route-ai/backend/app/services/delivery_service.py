"""DeliveryService encapsulating core business logic for delivery order management."""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.delivery_repository import delivery_repository
from app.schemas.delivery import (
    DeliveryCreate,
    DeliveryListResponse,
    DeliveryResponse,
    DeliveryUpdate,
)


class DeliveryService:
    """Service handling delivery operations, validation rules, and business logic."""

    VALID_STATUSES = {"pending", "scheduled", "assigned", "in_transit", "delivered", "failed", "cancelled"}

    def create_delivery(self, db: Session, create_data: DeliveryCreate) -> DeliveryResponse:
        """Process and create a new delivery order.

        Args:
            db: Database session.
            create_data: Validated DeliveryCreate Pydantic payload.

        Returns:
            DeliveryResponse containing newly created delivery details.
        """
        payload = create_data.model_dump()
        payload["delivery_status"] = "pending"

        delivery = delivery_repository.create_delivery(db, payload)
        return DeliveryResponse.model_validate(delivery)

    def get_delivery_by_id(self, db: Session, delivery_id: int) -> DeliveryResponse:
        """Fetch delivery details by primary key ID.

        Args:
            db: Database session.
            delivery_id: Primary key integer.

        Returns:
            DeliveryResponse schema.

        Raises:
            HTTPException: 404 Not Found if delivery does not exist.
        """
        delivery = delivery_repository.get_by_id(db, delivery_id)
        if not delivery:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Delivery with ID {delivery_id} was not found.",
            )
        return DeliveryResponse.model_validate(delivery)

    def list_deliveries(
        self,
        db: Session,
        *,
        page: int = 1,
        size: int = 20,
        delivery_status: Optional[str] = None,
        customer_id: Optional[int] = None,
    ) -> DeliveryListResponse:
        """Fetch paginated delivery records.

        Args:
            db: Database session.
            page: 1-indexed page number.
            size: Page size limit.
            delivery_status: Optional status string filter.
            customer_id: Optional customer ID filter.

        Returns:
            DeliveryListResponse paginated container.
        """
        if delivery_status and delivery_status not in self.VALID_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid delivery status '{delivery_status}'. Allowed values: {', '.join(sorted(self.VALID_STATUSES))}",
            )

        skip = (page - 1) * size
        items, total = delivery_repository.list_deliveries(
            db, skip=skip, limit=size, status=delivery_status, customer_id=customer_id
        )

        formatted_items = [DeliveryResponse.model_validate(item) for item in items]
        return DeliveryListResponse(
            total=total,
            page=page,
            size=size,
            items=formatted_items,
        )

    def update_delivery(
        self, db: Session, delivery_id: int, update_data: DeliveryUpdate
    ) -> DeliveryResponse:
        """Update fields of an existing delivery order.

        Args:
            db: Database session.
            delivery_id: Delivery primary key integer.
            update_data: DeliveryUpdate Pydantic schema with non-None values.

        Returns:
            Updated DeliveryResponse schema.

        Raises:
            HTTPException: 404 Not Found if delivery missing; 400 Bad Request if invalid status.
        """
        delivery = delivery_repository.get_by_id(db, delivery_id)
        if not delivery:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Delivery with ID {delivery_id} was not found.",
            )

        changes = update_data.model_dump(exclude_unset=True)

        if "delivery_status" in changes and changes["delivery_status"]:
            new_status = changes["delivery_status"]
            if new_status not in self.VALID_STATUSES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid delivery status '{new_status}'. Allowed values: {', '.join(sorted(self.VALID_STATUSES))}",
                )

        updated_delivery = delivery_repository.update_delivery(db, delivery, changes)
        return DeliveryResponse.model_validate(updated_delivery)

    def delete_delivery(self, db: Session, delivery_id: int) -> dict[str, str]:
        """Delete a delivery order by ID.

        Args:
            db: Database session.
            delivery_id: Primary key integer.

        Returns:
            Confirmation message dictionary.

        Raises:
            HTTPException: 404 Not Found if delivery missing.
        """
        delivery = delivery_repository.get_by_id(db, delivery_id)
        if not delivery:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Delivery with ID {delivery_id} was not found.",
            )

        delivery_repository.delete_delivery(db, delivery)
        return {"message": f"Delivery {delivery_id} successfully deleted."}


delivery_service = DeliveryService()
