from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def get_users_placeholder():
    return {'module': 'users', 'status': 'initialized'}
