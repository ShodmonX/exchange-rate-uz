import aiohttp
import json
import datetime

from shared import settings
from shared.utils import get_currency_map
from shared.schemas import ExchangeRateIn
from shared.db import LocalAsyncSession
from shared.db.crud import set_exchange_rate


async def get_data(url: str):
    data = []
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        if response.status == 200:
            html = await response.text()
            print(response.headers)
            if 'text/html' in response.headers['Content-Type']:
                json_data = json.loads(html)
            else:
                json_data = await response.json()
            if html is None:
                return
            
            if json_data is None:
                print("Data not found")
                return
            
            if not json_data.get('success', False):
                print("Failed to get data")
                return 
            
            data = json_data['data']['offline']
            result = await preprocces(data)
            
            return result

        else:
            print(f"Failed to fetch the page. Status code: {response.status}")

async def preprocces(data: list[dict]):
    result_data = []
    async with LocalAsyncSession() as session:
        currencies = await get_currency_map(session)
    for d in data:
        current_data = {
            "currency_id": currencies[d['code']],
            'buy_rate': d['buy'] / 100,
            'sell_rate': d['sell'] / 100,
            'bank_id': 3,
            'date': datetime.date.today()
        }
        result_data.append(current_data)
    return result_data

async def sqb_main():
    url = "https://sqb.uz/api/site-kurs-api/"

    data = await get_data(url)
    if data is None:
        async with aiohttp.ClientSession() as session:
            await session.get(f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage?chat_id={settings.TELEGRAM_ADMIN_ID}&text=O’zsanoatqurilishbank: Xatolik")
        return
    async with LocalAsyncSession() as session:
        for d in data:
            exchange_rate = ExchangeRateIn(**d)
            await set_exchange_rate(session, exchange_rate)
