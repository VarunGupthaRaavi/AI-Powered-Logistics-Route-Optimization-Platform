from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def get_rag_placeholder():
    return {'module': 'rag', 'status': 'initialized'}
