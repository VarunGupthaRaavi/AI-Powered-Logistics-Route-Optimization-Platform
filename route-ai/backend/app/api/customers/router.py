from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def get_customers_placeholder():
    return {'module': 'customers', 'status': 'initialized'}
