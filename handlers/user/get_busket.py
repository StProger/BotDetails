import re

from aiogram import Router, F, types, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboard import menu

from db_api.busket.api import Busket

import json

from utils.get_params import get_params, get_params_one_detail, params_select_item
from utils.params_busket import get_price_with_percent

from .get_detail import SGetDetail


get_busket_router = Router()


@get_busket_router.callback_query(StateFilter("*"), F.data == "get_basket")
async def content_busket(callback: types.CallbackQuery,
                         is_empty,
                         state: FSMContext):
    await state.clear()
    try:
        if is_empty:
            await callback.answer("Корзина пуста", show_alert=True)
        else:

            result = await Busket.get_items(user_id=callback.from_user.id, state=state)
            text = result[0]
            keyboard = result[1]
            text += "\n\nДля удаления товара из корзины нажмите на его номер снизу⬇️"
            await callback.message.delete()
            await callback.message.answer(
                text=text,
                reply_markup=keyboard
            )
    except Exception as ex:
        print(ex)
