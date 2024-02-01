from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboard import menu

from db_api.api import DatabaseAPI

import json

detail_router = Router()


class SGetDetail(StatesGroup):

    article = State()
    choose_producer = State()
    choose_item = State()


@detail_router.callback_query(F.data == "get_detail_menu")
async def get_article(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state(SGetDetail.article)
    await callback.message.delete()
    await callback.message.answer("Отправьте артикул желаемой детали.",
                                  reply_markup=menu.go_menu())


@detail_router.message(SGetDetail.article)
async def get_producer(message: types.Message, state: FSMContext, bot: Bot):

    if not(message.text.isdigit()):
        try:
            await bot.delete_message(
                chat_id=message.from_user.id,
                message_id=message.message_id-1
            )
        except:
            pass
        await message.delete()
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Вы ввели некорректный артикул, попробуйте ещё раз.",
            reply_markup=menu.go_menu()
        )

    result = await DatabaseAPI.get_data_for_articul(article=message.text, telegram_id=message.from_user.id)
    if not result:
        await message.answer("Нет деталей с таким артикулом, попробуйте другой артикул.",
                             reply_markup=menu.go_menu())

    else:
        with open(f"data/{message.from_user.id}_data.json", "r") as file:
            data = json.loads(file.read())

        names = []
        for key in data.keys():
            names.append(data[key][0]["Названия бренда"])
        await message.answer(
            text="Выберите производителя",
            reply_markup=menu.choose_producer_key(names=names)
        )
        await state.set_state(SGetDetail.choose_producer)


@detail_router.callback_query(SGetDetail.choose_producer)
async def choose_detail(callback: types.CallbackQuery, state: FSMContext):
    with open(f"data/{callback.from_user.id}_data.json", "r") as file:
        data = json.loads(file.read())
    choosed_producer = data.keys()[int(callback.data)]
