"""Delivery Management API router endpoints."""

from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.schemas.delivery import (
    DeliveryCreate,
    DeliveryListResponse,
    DeliveryResponse,
    DeliveryUpdate,
)
from app.security.dependencies import get_current_user, require_role
from app.services.delivery_service import delivery_service

router = APIRouter()


@router.post(
    "",
    response_model=DeliveryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new delivery order",
    description="Validates delivery order parameters, validates customer relationship, and creates a new pending delivery.",
)
def create_delivery(
    request: DeliveryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DeliveryResponse:
    """Create a new delivery order."""
    return delivery_service.create_delivery(db, request)


@router.get(
    "",
    response_model=DeliveryListResponse,
    status_code=status.HTTP_200_OK,
    summary="List paginated delivery orders",
    description="Fetch a paginated collection of deliveries with optional status and customer_id filters.",
)
def list_deliveries(
    page: int = Query(1, ge=1, description="Page number starting from 1"),
    size: int = Query(20, ge=1, le=100, description="Page size limit (max 100)"),
    delivery_status: Optional[str] = Query(None, alias="status", description="Filter by status (e.g. pending, in_transit)"),
    customer_id: Optional[int] = Query(None, description="Filter by customer ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DeliveryListResponse:
    """Retrieve paginated list of deliveries."""
    return delivery_service.list_deliveries(
        db, page=page, size=size, delivery_status=delivery_status, customer_id=customer_id
    )


@router.get(
    "/{id}",
    response_model=DeliveryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get delivery details by ID",
    description="Fetch full details for a single delivery by primary key ID.",
)
def get_delivery_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DeliveryResponse:
    """Get delivery details by primary key ID."""
    return delivery_service.get_delivery_by_id(db, id)


@router.put(
    "/{id}",
    response_model=DeliveryResponse,
    status_code=status.HTTP_200_OK,
    summary="Update delivery order",
    description="Update fields on an existing delivery order (status, vehicle, driver, pickup/drop locations, time windows).",
)
def update_delivery(
    id: int,
    request: DeliveryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DeliveryResponse:
    """Update an existing delivery order."""
    return delivery_service.update_delivery(db, id, request)


@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Delete delivery order (Admin only)",
    description="Deletes a delivery order from the system. Requires Admin role authorization.",
)
def delete_delivery(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
) -> dict[str, str]:
    """Delete a delivery order (Admin permission required)."""
    return delivery_service.delete_delivery(db, id)
