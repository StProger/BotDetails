from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware, types
from aiogram.types import TelegramObject

from db_api.busket.api import Busket


class BusketIsEmpty(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user_id = data["event_from_user"].id
        print(f"Middlware call: {user_id} ")

        busket_is_empty = await Busket.is_empty(user_id=user_id)
        print(f"Middlware call: {user_id} | {busket_is_empty}")
        if busket_is_empty:
            data["is_empty"] = True
        else:
            data["is_empty"] = False
        return await handler(event, data)
