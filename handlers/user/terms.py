from aiogram import Router, F, Bot, types

from db_api.api import DatabaseAPI

from keyboard import menu


terms_router = Router()


@terms_router.callback_query(F.data == "about_shop")
async def get_info_company(callback: types.CallbackQuery):

    about_company = await DatabaseAPI.get_about_company()

    await callback.message.delete()
    await callback.message.answer(
        text=about_company,
        reply_markup=menu.go_menu()
    )


@terms_router.callback_query(F.data == "info_refund")
async def get_info_refund(callback: types.CallbackQuery):
    refund_info = await DatabaseAPI.get_refund()

    await callback.message.delete()
    await callback.message.answer(
        text=refund_info,
        reply_markup=menu.go_menu()
    )