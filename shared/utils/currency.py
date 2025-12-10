from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from .redis_cache import cacher
from shared.db.models import Currency, Bank

@cacher(ttl=3600)
async def get_currency_map(session: AsyncSession):
    result = await session.execute(
        select(Currency.id, Currency.code)
    )
    return {code: id for id, code in result.all()}

@cacher(ttl=3600)
async def get_bank_map(session: AsyncSession):
    result = await session.execute(
        select(Bank.id, Bank.code)
    )
    return {code: id for id, code in result.all()}