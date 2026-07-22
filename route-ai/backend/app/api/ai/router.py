from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def get_ai_placeholder():
    return {'module': 'ai', 'status': 'initialized'}
