from fastapi import APIRouter, Depends

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/embeddings",
    tags=["embeddings"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_items():
    return fake_items_db
