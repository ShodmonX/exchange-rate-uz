from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from shared.db import get_db
from shared.db.crud import get_available_currencies, get_currency_by_code, get_exchange_rates_by_currency
from shared.schemas import CurrencyOut


router = APIRouter(
    prefix="/currency",
    tags=["Currency"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[CurrencyOut], summary="Get all available currencies")
async def get_all_currencies(db: AsyncSession = Depends(get_db)):
    return await get_available_currencies(db)

@router.get("/{currency_code}", response_model=CurrencyOut, summary="Get currency by code")
async def get_currency_rates(currency_code: str, db: AsyncSession = Depends(get_db)):
    currency_code = currency_code.upper()
    currency = await get_currency_by_code(db, currency_code)
    if not currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")
    return get_exchange_rates_by_currency(db, currency.id, True)