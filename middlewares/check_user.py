from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware, types
from aiogram.types import TelegramObject

from db_api.api import DatabaseAPI


class CheckUser(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        print(data)
        user_id = data["event_from_user"].id
        message: types.Message = data["event_update"].message


        if not(await DatabaseAPI.user_exist(telegram_id=user_id)):
            print("Регаю")
            await DatabaseAPI.register_user(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                name=message.from_user.first_name
            )

        return await handler(event, data)
