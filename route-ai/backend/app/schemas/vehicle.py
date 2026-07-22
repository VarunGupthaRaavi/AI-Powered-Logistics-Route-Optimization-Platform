from pydantic import BaseModel

class VehicleBase(BaseModel):
    license_plate: str
    capacity_kg: float

class VehicleResponse(VehicleBase):
    id: str
    class Config:
        from_attributes = True
