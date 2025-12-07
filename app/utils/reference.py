import json

from shared.utils import redis
from shared.db import LocalAsyncSession
from shared.db.crud import get_available_banks, get_available_currencies
from shared.schemas import BankOut, CurrencyOut

async def refresh_reference_cache():
    async with LocalAsyncSession() as session:
        banks = await get_available_banks(session)
        currencies = await get_available_currencies(session)

    banks_json = json.dumps([BankOut.model_validate(b).model_dump() for b in banks])
    currencies_json = json.dumps([CurrencyOut.model_validate(c).model_dump() for c in currencies])

    await redis.set("banks", banks_json)
    await redis.set("currencies", currencies_json)