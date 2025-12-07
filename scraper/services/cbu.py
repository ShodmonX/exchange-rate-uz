from aiohttp import ClientSession

import datetime
import json

from shared.db import LocalAsyncSession
from shared.db.crud import set_exchange_rate
from shared.schemas import ExchangeRateIn
from shared.utils import redis


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

async def add_db(data: list[dict]):
    async with LocalAsyncSession() as session:
        currencies = await redis.get("currencies")
        currencies = json.loads(currencies)
        for i in data:
            exchange_rate = ExchangeRateIn(
                date=datetime.date.today(),
                buy_rate=i['Rate'],
                sell_rate=i['Rate'],
                bank_id=1,
                currency_id=get_currency_id(i['Ccy'], currencies),
            )
            await set_exchange_rate(session, exchange_rate)

def get_currency_id(code: str, currencies: list[dict]):
    for c in currencies:
        if c['code'] == code:
            return c['id']
    return 1
        
async def cbu_main():
    data = await get_currencies()
    await add_db(data)
