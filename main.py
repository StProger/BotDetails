from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.methods import DeleteWebhook

import asyncio

import aioredis

from config import TOKEN_BOT, REDIS_URL

from handlers import main_router_user

import logging


async def main():

    bot = Bot(token=TOKEN_BOT, parse_mode="HTML")
    dp = Dispatcher(storage=RedisStorage(redis=aioredis.from_url(REDIS_URL)))
    await bot(DeleteWebhook())
    dp.include_routers(
        main_router_user
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())