from fastapi import APIRouter, Body, Depends

from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from shared.schemas import ExchangeRateIn, ExchangeRateOut
from shared.db import get_db
from shared.db.crud import set_exchange_rate, get_exchange_rates_today


router = APIRouter(
    prefix="/exchange_rate",
    tags=["Exchange Rate"],
    responses={404: {"description": "Not found"}},
)

@router.get("/today", response_model=list[ExchangeRateOut], summary="Get exchange rates for today")
async def get_exchange_rates_todays(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await get_exchange_rates_today(db)

@router.post("/", summary="Add exchange rate")
async def add_exchange_rate(
    exchange_rate: Annotated[ExchangeRateIn, Body(...)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    exchange_rate_db = await set_exchange_rate(db, exchange_rate)
    return exchange_rate_db