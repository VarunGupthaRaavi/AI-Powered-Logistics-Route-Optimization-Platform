from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def get_auth_placeholder():
    return {'module': 'auth', 'status': 'initialized'}
