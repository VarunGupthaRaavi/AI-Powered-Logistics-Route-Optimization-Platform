from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def get_deliveries_placeholder():
    return {'module': 'deliveries', 'status': 'initialized'}
