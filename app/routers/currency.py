from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
import json

from shared.db import get_db
from shared.db.crud import get_available_currencies
from shared.schemas import CurrencyOut


router = APIRouter(
    prefix="/currency",
    tags=["Currency"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[CurrencyOut], summary="Get all available currencies")
async def get_all_currencies(db: AsyncSession = Depends(get_db)):
    return await get_available_currencies(db)