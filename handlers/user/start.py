from aiogram import Router, types, Bot, F
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext

from keyboard import menu


start_router = Router()


@start_router.callback_query(F.data == "go_menu")
async def go_menu(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()

    await callback.message.delete()
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=types.FSInputFile("photo/logo.jpg"),
        reply_markup=menu.menu_key()
    )


@start_router.message(CommandStart())
async def cmd_start(message: types.Message, bot: Bot):

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


