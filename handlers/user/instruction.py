from aiogram import Router, F, types, Bot

from db_api.api import DatabaseAPI

from keyboard import menu


instr_router = Router()


@instr_router.callback_query(F.data == "get_instruct")
async def give_instruct(callback: types.CallbackQuery):

    instruction = await DatabaseAPI.get_instruction()
    await callback.message.delete()
    await callback.message.answer(
        text=instruction,
        reply_markup=menu.go_menu()
    )
