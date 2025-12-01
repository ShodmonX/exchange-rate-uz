from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
import asyncio

import logging

from shared import settings


router = Router()

@router.message()
async def echo(message: Message):
    if message.text is not None:
        await message.answer(message.text)

async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    asyncio.run(main())