from aiogram import Router, F, types, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db_api.api import DatabaseAPI

import json

from handlers.user.get_detail import SGetDetail
from utils.get_params import params_select_item

action_item_router = Router()


@action_item_router.callback_query(StateFilter("*"), F.data.contains("hash"))
async def handle_action_item(callback: types.CallbackQuery, state: FSMContext):

    hash_ = callback.data.split("_")[-1]

    hash_data = await DatabaseAPI.get_hash_data(hash_=hash_)

    data_json = {
        hash_data["link_item"]: [
            hash_data["product"]
        ]
    }

    with open(f"data/{callback.from_user.id}_data.json", "w") as file:

        json.dump(data_json, file)

    await state.update_data(
        choosed_producer=hash_data["link_item"],
        index_detail=0,
        count_product=1,
        choose_detail=hash_data["product"]
    )

    params_item = await params_select_item(hash_data["product"], state=state)

    builder = InlineKeyboardBuilder()
    builder.button(text="Добавить в корзину", callback_data=f"add_to_busket_0")
    builder.row(
        types.InlineKeyboardButton(
            text="➖", callback_data="action_minus_item_0"
        ),
        types.InlineKeyboardButton(
            text="1 шт.", callback_data="_"
        ),
        types.InlineKeyboardButton(
            text="➕", callback_data="action_plus_item_2"
        )
    )
    builder.row(
        types.InlineKeyboardButton(text="Оформить заказ", callback_data="go_order")
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Корзина", callback_data="get_basket"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Меню", callback_data="go_menu"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Ввести другой артикул", callback_data="get_detail_menu"
        )
    )

    await state.set_state(SGetDetail.order)
    print("Поставил стейт")
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer(
        text=params_item,
        reply_markup=builder.as_markup()
    )


