from fastapi import APIRouter
from twarc import Twarc

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.get("/{user_handle}")
async def search_get(user_handle: str):
    return {"tweets": user_handle}
