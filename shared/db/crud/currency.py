from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.models import Currency


async def get_available_currencies(db: AsyncSession):
    query = select(Currency)
    result = await db.execute(query)
    return result.scalars().all()