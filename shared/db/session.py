from sqlalchemy.ext.asyncio import AsyncSession

from typing import AsyncGenerator

from shared.db import LocalAsyncSession


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with LocalAsyncSession() as session:
        yield session