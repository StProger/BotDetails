from aiogram import Router, types, Bot, F
from aiogram.filters import StateFilter
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext

from keyboard import menu

import os

from filters import ChatTypeFilter


start_router = Router()


@start_router.callback_query(StateFilter("*"), F.data == "go_menu")
async def go_menu(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    if os.path.exists(f"data/{callback.from_user.id}_data.json"):
        os.remove(f"data/{callback.from_user.id}_data.json")
    if os.path.exists(f"data/{callback.from_user.id}_data_links.json"):
        os.remove(f"data/{callback.from_user.id}_data_links.json")
    await callback.message.delete()
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=types.FSInputFile("photo/logo.jpg"),
        reply_markup=menu.menu_key()
    )


@start_router.message(CommandStart())
async def cmd_start(message: types.Message, bot: Bot, state: FSMContext):
    await state.clear()

    if os.path.exists(f"data/{message.from_user.id}_data.json"):
        os.remove(f"data/{message.from_user.id}_data.json")
    if os.path.exists(f"data/{message.from_user.id}_data_links.json"):
        os.remove(f"data/{message.from_user.id}_data_links.json")
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id-1
        )
    except:
        pass
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=types.FSInputFile("photo/logo.jpg"),
        reply_markup=menu.menu_key()
    )


@start_router.callback_query(F.data == "go_menu_w")
async def go_menu(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    if os.path.exists(f"data/{callback.from_user.id}_data.json"):
        os.remove(f"data/{callback.from_user.id}_data.json")
    if os.path.exists(f"data/{callback.from_user.id}_data_links.json"):
        os.remove(f"data/{callback.from_user.id}_data_links.json")

    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=types.FSInputFile("photo/logo.jpg"),
        reply_markup=menu.menu_key()
    )
    await callback.answer()
