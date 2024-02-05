from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboard import menu

from db_api.api import DatabaseAPI

import json

from utils.get_params import get_params, get_params_one_detail

detail_router = Router()


class SGetDetail(StatesGroup):

    article = State()
    choose_producer = State()
    choose_item = State()
    order = State()


@detail_router.callback_query(F.data == "get_detail_menu")
async def get_article(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state(SGetDetail.article)
    await callback.message.delete()
    await callback.message.answer("Отправьте артикул желаемой детали.",
                                  reply_markup=menu.go_menu())


@detail_router.message(SGetDetail.article)
async def get_producer(message: types.Message, state: FSMContext, bot: Bot):

    clock_message = await message.answer("Идет поиск товара, подождите немного⏳")
    result = await DatabaseAPI.get_data_for_articul(article=message.text, telegram_id=message.from_user.id)
    if not result:
        await clock_message.delete()
        await message.answer("Нет деталей с таким артикулом, попробуйте другой артикул.",
                             reply_markup=menu.go_menu())
        return

    else:
        with open(f"data/{message.from_user.id}_data.json", "r") as file:
            data = json.loads(file.read())

        names = []
        for key in data.keys():
            names.append(data[key][0]["Названия бренда"])
        await clock_message.delete()
        await message.answer(
            text="Выберите производителя",
            reply_markup=menu.choose_producer_key(names=names)
        )
        await state.set_state(SGetDetail.choose_producer)


@detail_router.callback_query(SGetDetail.choose_producer, F.data == "back_to_prod")
async def get_producer(callback: types.CallbackQuery, state: FSMContext):
    with open(f"data/{callback.from_user.id}_data.json", "r") as file:
        data = json.loads(file.read())

    names = []
    for key in data.keys():
        names.append(data[key][0]["Названия бренда"])
    await callback.message.edit_text(
        text="Выберите производителя",
        reply_markup=menu.choose_producer_key(names=names)
    )
    await state.set_state(SGetDetail.choose_producer)


@detail_router.callback_query(SGetDetail.choose_producer)
async def choose_detail(callback: types.CallbackQuery, state: FSMContext):
    with open(f"data/{callback.from_user.id}_data.json", "r") as file:
        data = json.loads(file.read())
    choosed_producer = None
    for i, key in enumerate(data.keys()):
        if i == int(callback.data):
            choosed_producer = key
            break
    text = await get_params(data[choosed_producer])
    await state.update_data(choosed_producer=choosed_producer)
    await state.set_state(SGetDetail.choose_item)
    await callback.message.edit_text(
        text=text,
        reply_markup=menu.choose_item_key()
    )


@detail_router.callback_query(SGetDetail.choose_item)
async def go_order(callback: types.CallbackQuery, state: FSMContext):

    state_data = await state.get_data()
    choosed_producer = state_data["choosed_producer"]

    with open(f"data/{callback.from_user.id}_data.json", "r") as file:
        data = json.loads(file.read())

    choose_detail = data[choosed_producer][int(callback.data)]
    await state.set_state(SGetDetail.order)
    text = await get_params_one_detail(choose_detail)
    await callback.message.edit_text(
        text=text,
        reply_markup=menu.key_order()
    )


@detail_router.callback_query(SGetDetail.order, F.data == "back_to_choose_detail")
async def back_to_choose_detail(callback: types.CallbackQuery, state: FSMContext):

    state_data = await state.get_data()
    choosed_producer = state_data["choosed_producer"]
    with open(f"data/{callback.from_user.id}_data.json", "r") as file:
        data = json.loads(file.read())
    text = await get_params(data[choosed_producer])
    await state.set_state(SGetDetail.choose_item)
    await callback.message.edit_text(
        text=text,
        reply_markup=menu.choose_item_key()
    )