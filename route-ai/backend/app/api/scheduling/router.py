from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def get_scheduling_placeholder():
    return {'module': 'scheduling', 'status': 'initialized'}
