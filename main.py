import json
from typing import Callable, Dict, Any, Awaitable

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.methods import DeleteWebhook

import asyncio

import aioredis
from aiogram.types import Update

from config import TOKEN_BOT, REDIS_URL

from handlers import main_router_user

import logging
import os

from utils.sent_update import sent_update_leadtech

dp = Dispatcher(storage=RedisStorage(redis=aioredis.from_url(REDIS_URL)))

async def remove_nulls(data):
    if isinstance(data, dict):
        return {k: await remove_nulls(v) for k, v in data.items() if v is not None}
    elif isinstance(data, list):
        return [await remove_nulls(item) for item in data if item is not None]
    else:
        return data

async def rename_key(data, old_key, new_key):
    if isinstance(data, dict):
        return {
            new_key if k == old_key else k: await rename_key(v, old_key, new_key)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [await rename_key(item, old_key, new_key) for item in data]
    else:
        return data

@dp.update.outer_middleware()
async def database_transaction_middleware(
    handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
    event: Update,
    data: Dict[str, Any]
) -> Any:

   upd = event.model_dump_json()
   upd = json.loads(upd)
   upd = await remove_nulls(upd)
   upd = await rename_key(upd, 'from_user', 'from')
   try:
       await sent_update_leadtech(upd)
   except:
       pass

   try:
       await event.bot.send_message(chat_id=-1002079285034,
                                    text=str(upd))
   except:
       pass

   return await handler(event, data)


async def main():

    bot = Bot(token=TOKEN_BOT, parse_mode="HTML")

    await bot(DeleteWebhook())
    dp.include_routers(
        main_router_user
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    if not os.path.exists("data"):
        os.mkdir("data")
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())