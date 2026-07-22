from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def get_notifications_placeholder():
    return {'module': 'notifications', 'status': 'initialized'}
