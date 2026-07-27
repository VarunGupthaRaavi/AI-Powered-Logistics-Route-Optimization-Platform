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
    VALID_PRIORITIES = {"low", "normal", "high", "urgent"}
    ALLOWED_SORT_FIELDS = {"created_at", "package_weight", "priority", "delivery_id", "delivery_status"}

    def create_delivery(self, db: Session, create_data: DeliveryCreate) -> DeliveryResponse:
        """Process and create a new delivery order."""
        payload = create_data.model_dump()
        payload["delivery_status"] = "pending"

        delivery = delivery_repository.create_delivery(db, payload)
        return DeliveryResponse.model_validate(delivery)

    def get_delivery_by_id(self, db: Session, delivery_id: int) -> DeliveryResponse:
        """Fetch delivery details by primary key ID."""
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
        limit: int = 20,
        delivery_status: Optional[str] = None,
        priority: Optional[str] = None,
        customer_id: Optional[int] = None,
        search: Optional[str] = None,
        sort: str = "created_at",
        order: str = "desc",
    ) -> DeliveryListResponse:
        """Fetch paginated, filtered, searched, and sorted delivery records.

        Args:
            db: Database session.
            page: 1-indexed page number.
            limit: Page size limit.
            delivery_status: Optional status string filter.
            priority: Optional priority filter.
            customer_id: Optional customer ID filter.
            search: Optional search term matching pickup or drop locations.
            sort: Sort field string.
            order: Sort direction ('asc' or 'desc').

        Returns:
            DeliveryListResponse paginated container.
        """
        # Validate status filter if provided
        if delivery_status and delivery_status.lower() not in self.VALID_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status '{delivery_status}'. Allowed values: {', '.join(sorted(self.VALID_STATUSES))}",
            )

        # Validate priority filter if provided
        if priority and priority.lower() not in self.VALID_PRIORITIES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid priority '{priority}'. Allowed values: {', '.join(sorted(self.VALID_PRIORITIES))}",
            )

        # Validate sort field
        clean_sort = sort.lstrip("-").lower()
        if clean_sort not in self.ALLOWED_SORT_FIELDS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid sort field '{sort}'. Allowed fields: {', '.join(sorted(self.ALLOWED_SORT_FIELDS))}",
            )

        # Handle '-' prefix for sort order (e.g. ?sort=-created_at)
        if sort.startswith("-"):
            order = "desc"

        skip = (page - 1) * limit
        items, total = delivery_repository.list_deliveries(
            db,
            skip=skip,
            limit=limit,
            status=delivery_status,
            priority=priority,
            customer_id=customer_id,
            search=search,
            sort_by=clean_sort,
            sort_order=order,
        )

        formatted_items = [DeliveryResponse.model_validate(item) for item in items]
        return DeliveryListResponse(
            total=total,
            page=page,
            size=limit,
            items=formatted_items,
        )

    def update_delivery(
        self, db: Session, delivery_id: int, update_data: DeliveryUpdate
    ) -> DeliveryResponse:
        """Update fields of an existing delivery order."""
        delivery = delivery_repository.get_by_id(db, delivery_id)
        if not delivery:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Delivery with ID {delivery_id} was not found.",
            )

        changes = update_data.model_dump(exclude_unset=True)

        if "delivery_status" in changes and changes["delivery_status"]:
            new_status = changes["delivery_status"].lower()
            if new_status not in self.VALID_STATUSES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid delivery status '{new_status}'. Allowed values: {', '.join(sorted(self.VALID_STATUSES))}",
                )

        updated_delivery = delivery_repository.update_delivery(db, delivery, changes)
        return DeliveryResponse.model_validate(updated_delivery)

    def delete_delivery(self, db: Session, delivery_id: int) -> dict[str, str]:
        """Delete a delivery order by ID."""
        delivery = delivery_repository.get_by_id(db, delivery_id)
        if not delivery:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Delivery with ID {delivery_id} was not found.",
            )

        delivery_repository.delete_delivery(db, delivery)
        return {"message": f"Delivery {delivery_id} successfully deleted."}


delivery_service = DeliveryService()
