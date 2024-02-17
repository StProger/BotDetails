import re

from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboard import menu

from db_api.busket.api import Busket

import json

from utils.get_params import get_params, get_params_one_detail, params_select_item
from utils.params_busket import get_price_with_percent

from .get_detail import SGetDetail



busket_router = Router()


class SBusket(StatesGroup):

    article = State()
    choose_producer = State()
    choose_item = State()
    order = State()
    order_only = State()
    point_pickup = State()
    contacts = State()
    photo_pay = State()
    note = State()


@busket_router.callback_query(SGetDetail.order, F.data == "add_to_busket")
async def add_item_to_busket(callback: types.CallbackQuery, state: FSMContext):

    state_data = await state.get_data()
    choosed_producer = state_data["choosed_producer"]

    with open(f"data/{callback.from_user.id}_data.json", "r") as file:
        data = json.loads(file.read())

    choose_detail = data[choosed_producer][int(callback.data.split("_")[-1])]
    choosed_producer = state_data["choosed_producer"]
    price_item = await get_price_with_percent(item=choose_detail)
    await Busket.add_item(item=choose_detail,
                          price=price_item,
                          link_item=choosed_producer,
                          user_id=callback.from_user.id)
    await callback.answer("Товар добавлен в корзину✅", show_alert=True)



