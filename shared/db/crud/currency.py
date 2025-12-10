from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.models import Currency


async def get_available_currencies(db: AsyncSession):
    query = select(Currency)
    result = await db.execute(query)
    return result.scalars().all()

async def get_currency_by_code(db: AsyncSession, code: str):
    query = select(Currency).where(Currency.code == code)
    result = await db.execute(query)
    return result.scalars().first()