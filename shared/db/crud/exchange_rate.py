from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import date

from shared.db.models import ExchangeRate
from shared.schemas import ExchangeRateIn


async def get_exchange_rates_by_currency(db: AsyncSession, currency_id: int):
    query = select(ExchangeRate).options(
        joinedload(ExchangeRate.currency),
        joinedload(ExchangeRate.bank),
    ).where(ExchangeRate.currency_id == currency_id)
    result = await db.execute(query)
    return result.scalars().all()

async def get_exchange_rates_by_bank(db: AsyncSession, bank_id: int):
    query = select(ExchangeRate).options(
        joinedload(ExchangeRate.currency),
        joinedload(ExchangeRate.bank),
    ).where(ExchangeRate.bank_id == bank_id)
    result = await db.execute(query)
    return result.scalars().all()

async def get_exchange_rates_today(db: AsyncSession):
    today = date.today()
    query = select(ExchangeRate).options(
        joinedload(ExchangeRate.currency),
        joinedload(ExchangeRate.bank),
    ).where(ExchangeRate.date == today)
    result = await db.execute(query)
    return result.scalars().all()

async def set_exchange_rate(db: AsyncSession, exchange_rate: ExchangeRateIn):
    exchange_rate_db = ExchangeRate(**exchange_rate.model_dump())
    try:
        db.add(exchange_rate_db)
        await db.commit()
        await db.refresh(exchange_rate_db)
        return exchange_rate_db
    except Exception as e:
        await db.rollback()
        raise e