from aiohttp import ClientSession

import datetime

from shared.db import LocalAsyncSession
from shared.db.crud import set_exchange_rate
from shared.schemas import ExchangeRateIn
from shared.utils import get_currency_map


async def get_currencies():
    currencies_id = [69, 21, 57, 22, 33, 38, 15, 14]
    data = []
    async with ClientSession() as session:
        async with session.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/") as response:
            response = await response.json()
            for currency in response:
                if currency['id'] in currencies_id:
                    data.append(currency)
    
    return data

async def add_db(data):
    async with LocalAsyncSession() as session:
        currency_map = await get_currency_map(session)

        for row in data:
            code = row["Ccy"]
            cid = currency_map.get(code)

            if not cid:
                continue

            exchange_rate = ExchangeRateIn(
                date=datetime.date.today(),
                buy_rate=row["Rate"],
                sell_rate=row["Rate"],
                bank_id=1,
                currency_id=cid
            )
            await set_exchange_rate(session, exchange_rate)

        await session.commit()

        
async def cbu_main():
    data = await get_currencies()
    await add_db(data)
