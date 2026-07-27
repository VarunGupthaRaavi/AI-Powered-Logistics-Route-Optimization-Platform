"""DeliveryService encapsulating core business logic and state machine validation for delivery management."""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import (
    DuplicateRecordException,
    EntityNotFoundException,
    IllegalStateTransitionException,
)
from app.repositories.delivery_repository import delivery_repository
from app.schemas.delivery import (
    DeliveryCreate,
    DeliveryListResponse,
    DeliveryResponse,
    DeliveryUpdate,
)


class DeliveryService:
    """Service handling delivery operations, business validation rules, and FSM transitions."""

    VALID_STATUSES = {"pending", "scheduled", "assigned", "in_transit", "delivered", "failed", "cancelled"}
    VALID_PRIORITIES = {"low", "normal", "high", "urgent"}
    ALLOWED_SORT_FIELDS = {"created_at", "package_weight", "priority", "delivery_id", "delivery_status"}

    # Permitted Finite State Machine (FSM) state transitions
    ALLOWED_TRANSITIONS = {
        "pending": {"scheduled", "cancelled"},
        "scheduled": {"assigned", "cancelled"},
        "assigned": {"in_transit", "cancelled"},
        "in_transit": {"delivered", "failed"},
        "delivered": set(),  # Terminal state
        "failed": set(),     # Terminal state
        "cancelled": set(),  # Terminal state
    }

    def validate_status_transition(self, current_status: str, new_status: str) -> None:
        """Validate whether a state transition from current_status to new_status is permitted.

        Args:
            current_status: Current delivery status string.
            new_status: Desired target delivery status string.

        Raises:
            IllegalStateTransitionException: 400 Bad Request if state transition is illegal.
        """
        curr = current_status.lower()
        target = new_status.lower()

        if curr == target:
            return  # Idempotent status update is permitted

        allowed_targets = self.ALLOWED_TRANSITIONS.get(curr, set())
        if target not in allowed_targets:
            raise IllegalStateTransitionException(
                current_status=current_status,
                target_status=new_status,
                allowed_targets=allowed_targets,
            )

    def create_delivery(self, db: Session, create_data: DeliveryCreate) -> DeliveryResponse:
        """Process and create a new delivery order after checking for duplicates.

        Args:
            db: Database session.
            create_data: Validated DeliveryCreate Pydantic payload.

        Returns:
            DeliveryResponse schema.

        Raises:
            DuplicateRecordException: 409 Conflict if active duplicate order already exists.
        """
        duplicate = delivery_repository.find_duplicate_delivery(
            db,
            customer_id=create_data.customer_id,
            pickup_location=create_data.pickup_location,
            drop_location=create_data.drop_location,
        )
        if duplicate:
            raise DuplicateRecordException(
                detail=f"An active delivery order (ID #{duplicate.delivery_id}) already exists for this customer with identical pickup and drop-off locations."
            )

        payload = create_data.model_dump()
        payload["delivery_status"] = "pending"

        delivery = delivery_repository.create_delivery(db, payload)
        return DeliveryResponse.model_validate(delivery)

    def get_delivery_by_id(self, db: Session, delivery_id: int) -> DeliveryResponse:
        """Fetch delivery details by primary key ID."""
        delivery = delivery_repository.get_by_id(db, delivery_id)
        if not delivery:
            raise EntityNotFoundException(entity_name="Delivery", entity_id=delivery_id)
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
        """Fetch paginated, filtered, searched, and sorted delivery records."""
        if delivery_status and delivery_status.lower() not in self.VALID_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status '{delivery_status}'. Allowed values: {', '.join(sorted(self.VALID_STATUSES))}",
            )

        if priority and priority.lower() not in self.VALID_PRIORITIES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid priority '{priority}'. Allowed values: {', '.join(sorted(self.VALID_PRIORITIES))}",
            )

        clean_sort = sort.lstrip("-").lower()
        if clean_sort not in self.ALLOWED_SORT_FIELDS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid sort field '{sort}'. Allowed fields: {', '.join(sorted(self.ALLOWED_SORT_FIELDS))}",
            )

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
        """Update fields on an existing delivery order with FSM transition validation."""
        delivery = delivery_repository.get_by_id(db, delivery_id)
        if not delivery:
            raise EntityNotFoundException(entity_name="Delivery", entity_id=delivery_id)

        changes = update_data.model_dump(exclude_unset=True)

        if "delivery_status" in changes and changes["delivery_status"]:
            new_status = changes["delivery_status"].lower()
            if new_status not in self.VALID_STATUSES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid delivery status '{new_status}'. Allowed values: {', '.join(sorted(self.VALID_STATUSES))}",
                )

            self.validate_status_transition(delivery.delivery_status, new_status)

        updated_delivery = delivery_repository.update_delivery(db, delivery, changes)
        return DeliveryResponse.model_validate(updated_delivery)

    def delete_delivery(self, db: Session, delivery_id: int) -> dict[str, str]:
        """Delete a delivery order by ID."""
        delivery = delivery_repository.get_by_id(db, delivery_id)
        if not delivery:
            raise EntityNotFoundException(entity_name="Delivery", entity_id=delivery_id)

        delivery_repository.delete_delivery(db, delivery)
        return {"message": f"Delivery {delivery_id} successfully deleted."}


delivery_service = DeliveryService()
