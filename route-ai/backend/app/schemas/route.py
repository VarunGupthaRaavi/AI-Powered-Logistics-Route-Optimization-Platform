from pydantic import BaseModel

class RouteBase(BaseModel):
    status: str = 'planned'

class RouteResponse(RouteBase):
    id: str
    class Config:
        from_attributes = True
