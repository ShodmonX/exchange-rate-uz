from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.models import Bank


async def get_available_banks(db: AsyncSession):
    query = select(Bank)
    result = await db.execute(query)
    return result.scalars().all()