from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from shared.db import get_db
from shared.db.crud import get_available_banks, get_exchange_rates_by_bank, get_bank_by_code
from shared.schemas import BankOut, ExchangeRateOut


router = APIRouter(
    prefix="/bank",
    tags=["Bank"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[BankOut], summary="Get all available banks")
async def get_all_banks(db: AsyncSession = Depends(get_db)):
    return await get_available_banks(db)

@router.get("/{bank_code}", response_model=list[ExchangeRateOut], summary="Get exchange rates by bank")
async def get_exchange_rates_by_banks(bank_code: str, db: AsyncSession = Depends(get_db)):
    bank_code = bank_code.upper()
    bank = await get_bank_by_code(db, bank_code)
    if not bank:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bank not found")
    return await get_exchange_rates_by_bank(db, bank.id, True)
    