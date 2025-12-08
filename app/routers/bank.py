from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
import json

from shared.db import get_db
from shared.db.crud import get_available_banks
from shared.schemas import BankOut


router = APIRouter(
    prefix="/bank",
    tags=["Bank"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[BankOut], summary="Get all available banks")
async def get_all_banks(db: AsyncSession = Depends(get_db)):
    return await get_available_banks(db)
    