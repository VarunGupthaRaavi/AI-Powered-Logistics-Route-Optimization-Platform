from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.customers import router as customers_router
from app.api.drivers import router as drivers_router
from app.api.vehicles import router as vehicles_router
from app.api.deliveries import router as deliveries_router
from app.api.routes import router as routes_router
from app.api.scheduling import router as scheduling_router
from app.api.analytics import router as analytics_router
from app.api.ai import router as ai_router
from app.api.rag import router as rag_router
from app.api.notifications import router as notifications_router

api_router = APIRouter()
api_router.include_router(auth_router.router, prefix='/auth', tags=['Auth'])
api_router.include_router(users_router.router, prefix='/users', tags=['Users'])
api_router.include_router(customers_router.router, prefix='/customers', tags=['Customers'])
api_router.include_router(drivers_router.router, prefix='/drivers', tags=['Drivers'])
api_router.include_router(vehicles_router.router, prefix='/vehicles', tags=['Vehicles'])
api_router.include_router(deliveries_router.router, prefix='/deliveries', tags=['Deliveries'])
api_router.include_router(routes_router.router, prefix='/routes', tags=['Routes'])
api_router.include_router(scheduling_router.router, prefix='/scheduling', tags=['Scheduling'])
api_router.include_router(analytics_router.router, prefix='/analytics', tags=['Analytics'])
api_router.include_router(ai_router.router, prefix='/ai', tags=['Ai'])
api_router.include_router(rag_router.router, prefix='/rag', tags=['Rag'])
api_router.include_router(notifications_router.router, prefix='/notifications', tags=['Notifications'])
