from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.methods import DeleteWebhook

import asyncio

from aioredis import Redis

from config import TOKEN_BOT

from handlers import main_router_user

import logging


async def main():

    bot = Bot(token=TOKEN_BOT, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())
    await bot(DeleteWebhook(drop_pending_updates=True))
    dp.include_routers(
        main_router_user
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())