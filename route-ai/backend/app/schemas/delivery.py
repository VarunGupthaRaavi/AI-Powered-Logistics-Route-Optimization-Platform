from pydantic import BaseModel

class DeliveryBase(BaseModel):
    destination: str
    status: str = 'pending'

class DeliveryResponse(DeliveryBase):
    id: str
    class Config:
        from_attributes = True
