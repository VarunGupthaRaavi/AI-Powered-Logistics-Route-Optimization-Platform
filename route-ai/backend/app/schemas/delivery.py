"""Pydantic schemas for Delivery request validation and response serialization."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DeliveryBase(BaseModel):
    """Base schema sharing common delivery attributes."""

    pickup_location: str = Field(..., min_length=3, max_length=500, description="Pickup address or depot location")
    drop_location: str = Field(..., min_length=3, max_length=500, description="Destination delivery address")
    package_weight: float = Field(..., gt=0, description="Package weight in kilograms")
    priority: str = Field("normal", description="Delivery priority: low, normal, high, urgent")
    delivery_window_start: Optional[datetime] = Field(None, description="Start time for delivery window")
    delivery_window_end: Optional[datetime] = Field(None, description="End time for delivery window")


class DeliveryCreate(DeliveryBase):
    """Payload schema for creating a new delivery order."""

    customer_id: int = Field(..., gt=0, description="Foreign key ID of the customer placing the order")
    vehicle_id: Optional[int] = Field(None, gt=0, description="Optional assigned vehicle ID")
    driver_id: Optional[int] = Field(None, gt=0, description="Optional assigned driver ID")


class DeliveryUpdate(BaseModel):
    """Payload schema for updating existing delivery attributes (all fields optional)."""

    pickup_location: Optional[str] = Field(None, min_length=3, max_length=500)
    drop_location: Optional[str] = Field(None, min_length=3, max_length=500)
    package_weight: Optional[float] = Field(None, gt=0)
    priority: Optional[str] = Field(None)
    delivery_window_start: Optional[datetime] = Field(None)
    delivery_window_end: Optional[datetime] = Field(None)
    delivery_status: Optional[str] = Field(None, description="Updated delivery status (e.g. pending, in_transit, delivered)")
    vehicle_id: Optional[int] = Field(None, gt=0)
    driver_id: Optional[int] = Field(None, gt=0)


class DeliveryResponse(DeliveryBase):
    """Response DTO schema representing full delivery details."""

    model_config = ConfigDict(from_attributes=True)

    delivery_id: int = Field(..., description="Primary key ID of the delivery")
    customer_id: int = Field(..., description="Customer ID")
    vehicle_id: Optional[int] = Field(None, description="Vehicle ID")
    driver_id: Optional[int] = Field(None, description="Driver ID")
    delivery_status: str = Field(..., description="Current delivery status")
    created_at: datetime = Field(..., description="Timestamp when order was created")


class DeliveryListResponse(BaseModel):
    """Paginated collection response for deliveries."""

    total: int = Field(..., description="Total number of deliveries matching filter")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Number of items per page")
    items: list[DeliveryResponse] = Field(..., description="List of delivery records")
