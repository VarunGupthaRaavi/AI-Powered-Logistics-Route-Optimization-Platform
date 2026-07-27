"""Pydantic schemas for Delivery request validation and response serialization with custom validators."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class DeliveryBase(BaseModel):
    """Base schema sharing common delivery attributes with Pydantic validation rules."""

    pickup_location: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Pickup address or depot location",
        examples=["Central Depot Hub, Hyderabad"],
    )
    drop_location: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Destination delivery address",
        examples=["Hitec City Phase 2, Hyderabad"],
    )
    package_weight: float = Field(
        ...,
        gt=0.0,
        le=1000.0,
        description="Package weight in kilograms (0.1 kg to 1000 kg)",
    )
    priority: str = Field(
        "normal",
        description="Delivery priority: low, normal, high, urgent",
    )
    delivery_window_start: Optional[datetime] = Field(
        None,
        description="Start time for delivery window",
    )
    delivery_window_end: Optional[datetime] = Field(
        None,
        description="End time for delivery window",
    )

    @field_validator("pickup_location", "drop_location")
    @classmethod
    def sanitize_and_validate_location(cls, value: str) -> str:
        """Strip whitespace and enforce minimum length after stripping."""
        cleaned = value.strip()
        if len(cleaned) < 3:
            raise ValueError("Location address must be at least 3 characters long after stripping whitespace.")
        return cleaned

    @field_validator("priority")
    @classmethod
    def validate_priority_value(cls, value: str) -> str:
        """Enforce permitted priority values."""
        allowed = {"low", "normal", "high", "urgent"}
        cleaned = value.strip().lower()
        if cleaned not in allowed:
            raise ValueError(f"Priority '{value}' is invalid. Allowed values: {', '.join(sorted(allowed))}")
        return cleaned

    @model_validator(mode="after")
    def validate_cross_field_rules(self) -> "DeliveryBase":
        """Cross-field business validation: pickup vs drop location and delivery time windows."""
        # Rule 1: Pickup location cannot be identical to drop location
        if self.pickup_location.lower() == self.drop_location.lower():
            raise ValueError("Pickup location and drop-off destination cannot be identical.")

        # Rule 2: Delivery window end time must be strictly after start time
        if self.delivery_window_start and self.delivery_window_end:
            if self.delivery_window_end <= self.delivery_window_start:
                raise ValueError("Delivery window end time must be after delivery window start time.")

        return self


class DeliveryCreate(DeliveryBase):
    """Payload schema for creating a new delivery order."""

    customer_id: int = Field(..., gt=0, description="Foreign key ID of customer placing order")
    vehicle_id: Optional[int] = Field(None, gt=0, description="Optional assigned vehicle ID")
    driver_id: Optional[int] = Field(None, gt=0, description="Optional assigned driver ID")


class DeliveryUpdate(BaseModel):
    """Payload schema for updating existing delivery attributes (all fields optional)."""

    pickup_location: Optional[str] = Field(None, min_length=3, max_length=500)
    drop_location: Optional[str] = Field(None, min_length=3, max_length=500)
    package_weight: Optional[float] = Field(None, gt=0.0, le=1000.0)
    priority: Optional[str] = Field(None)
    delivery_window_start: Optional[datetime] = Field(None)
    delivery_window_end: Optional[datetime] = Field(None)
    delivery_status: Optional[str] = Field(None, description="Updated delivery status")
    vehicle_id: Optional[int] = Field(None, gt=0)
    driver_id: Optional[int] = Field(None, gt=0)

    @field_validator("pickup_location", "drop_location")
    @classmethod
    def sanitize_optional_location(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            cleaned = value.strip()
            if len(cleaned) < 3:
                raise ValueError("Location address must be at least 3 characters long.")
            return cleaned
        return value


class DeliveryResponse(DeliveryBase):
    """Response DTO schema representing full delivery details."""

    model_config = ConfigDict(from_attributes=True)

    delivery_id: int = Field(..., description="Primary key ID of delivery")
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
