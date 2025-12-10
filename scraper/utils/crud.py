from sqlalchemy.ext.asyncio import AsyncSession

from shared.schemas import ExchangeRateIn
from shared.db.crud import set_exchange_rate


async def add_db(data: list[dict], session: AsyncSession):
    for row in data:
        exchange_rate = ExchangeRateIn(**row)
        await set_exchange_rate(session, exchange_rate)