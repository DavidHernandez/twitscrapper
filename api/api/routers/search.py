from fastapi import APIRouter

router = APIRouter(
    prefix='/search',
    tags=['search']
)

@router.get("/")
async def search_list():
    return {"data": []}

@router.get("/{search_id}")
async def search_get(search_id):
    return {"data": []}

@router.post("/")
async def search_post():
    return {"status": "Ok"}
