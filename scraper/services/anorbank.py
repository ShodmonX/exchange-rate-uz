import aiohttp
import datetime
from bs4 import BeautifulSoup
from bs4.element import Tag

from shared.utils import get_currency_map
from shared.db import LocalAsyncSession
from shared.db.crud import set_exchange_rate
from shared.schemas import ExchangeRateIn
from shared import settings


async def get_data(url: str):
    data = []
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        if response.status == 200:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            exchange_rate_div = soup.find("div", class_ = "exchange-rate")
            if exchange_rate_div is None:
                return
            exchange_rate_table = exchange_rate_div.find('tbody')
            if exchange_rate_table is None:
                return
            trs = exchange_rate_table.find_all('tr', recursive=False)
            if trs is None:
                return
            
            usd_data = await get_usd(trs[0])
            data.append(usd_data)
            for tr in trs[1:]:
                data.append(await get_others(tr))
            return data
        else:
            print(f"Failed to fetch the page. Status code: {response.status}")

async def get_usd(soup: BeautifulSoup | Tag):
    buy_rate_div = soup.find("div", class_="block-1")
    if buy_rate_div is None:
        print("Buy rate not found - USD")
        return
    buy_rate_text = buy_rate_div.text.strip()
    buy_rate = float(buy_rate_text.replace(",", ".").replace(" ", ""))

    sell_rate = soup.find("div", class_="block-2")
    if sell_rate is None:
        print("Sell rate not found - USD")
        return
    sell_rate_text = sell_rate.text.strip()
    sell_rate = float(sell_rate_text.replace(",", ".").replace(" ", ""))
    async with LocalAsyncSession() as session:
        currencies = await get_currency_map(session)
        currency_id = currencies.get("USD", 1)
    data = {
        "date": datetime.date.today().strftime("%Y-%m-%d"),
        "currency_id": currency_id,
        "buy_rate": buy_rate,
        "sell_rate": sell_rate,
        "bank_id": 2
    }

    return data

async def get_others(soup: BeautifulSoup | Tag):
    tds = soup.find_all("td")
    currency = tds[0].text.strip().split(",")[1].strip()
    buy_rate = float(tds[1].text.strip().replace(",", ".").replace(" ", ""))
    sell_rate = float(tds[2].text.strip().replace(",", ".").replace(" ", ""))
    async with LocalAsyncSession() as session:
        currencies = await get_currency_map(session)
        currency_id = currencies.get(currency, 1)
    data = {
        "date": datetime.date.today().strftime("%Y-%m-%d"),
        "currency_id": currency_id,
        "buy_rate": buy_rate,
        "sell_rate": sell_rate,
        "bank_id": 2
    }
    return data

async def anorbank_main():
    url = "https://anorbank.uz/uz/about/exchange-rates/"
    data = await get_data(url)
    if data is None:
        async with aiohttp.ClientSession() as session:
            await session.get(f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage?chat_id={settings.TELEGRAM_ADMIN_ID}&text=Anorbank: Xatolik")
        return
    async with LocalAsyncSession() as session:
        for d in data:
            exchange_rate = ExchangeRateIn(**d)
            await set_exchange_rate(session, exchange_rate)


