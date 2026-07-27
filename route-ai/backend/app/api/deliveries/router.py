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
    summary="List paginated, searched, filtered, and sorted delivery orders",
    description="Fetch a paginated collection of deliveries with optional search term, status, priority, customer_id, and sort options.",
)
def list_deliveries(
    page: int = Query(1, ge=1, description="Page number starting from 1"),
    limit: int = Query(20, ge=1, le=100, alias="limit", description="Number of items per page (max 100)"),
    status: Optional[str] = Query(None, description="Filter by status (e.g., Pending, In_Transit, Delivered)"),
    priority: Optional[str] = Query(None, description="Filter by priority (e.g., Low, Normal, High, Urgent)"),
    search: Optional[str] = Query(None, description="Search term matching pickup or drop locations"),
    customer_id: Optional[int] = Query(None, description="Filter by customer ID"),
    sort: str = Query("created_at", description="Field to sort by: created_at, package_weight, priority, delivery_id"),
    order: str = Query("desc", pattern="^(asc|desc|ASC|DESC)$", description="Sort direction: asc or desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DeliveryListResponse:
    """Retrieve paginated, searched, filtered, and sorted list of deliveries."""
    return delivery_service.list_deliveries(
        db,
        page=page,
        limit=limit,
        delivery_status=status,
        priority=priority,
        customer_id=customer_id,
        search=search,
        sort=sort,
        order=order,
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
