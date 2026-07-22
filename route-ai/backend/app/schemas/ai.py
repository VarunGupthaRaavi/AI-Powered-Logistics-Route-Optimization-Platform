from pydantic import BaseModel
from typing import List, Optional

class RouteOptimizeRequest(BaseModel):
    delivery_ids: List[str]
    vehicle_ids: List[str]

class RouteOptimizeResponse(BaseModel):
    status: str
    total_distance_km: float
    estimated_time_minutes: float
    optimized_routes: List[dict]
