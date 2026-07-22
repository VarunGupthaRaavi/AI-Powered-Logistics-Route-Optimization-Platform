from pydantic import BaseModel

class DriverBase(BaseModel):
    name: str
    status: str = 'available'

class DriverResponse(DriverBase):
    id: str
    class Config:
        from_attributes = True
