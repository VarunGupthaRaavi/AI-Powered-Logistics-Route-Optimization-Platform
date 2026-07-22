from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def get_vehicles_placeholder():
    return {'module': 'vehicles', 'status': 'initialized'}
