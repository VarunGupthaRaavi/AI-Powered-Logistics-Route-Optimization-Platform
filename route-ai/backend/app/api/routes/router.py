from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def get_routes_placeholder():
    return {'module': 'routes', 'status': 'initialized'}
