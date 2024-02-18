from aiogram import Router, Bot, F, types
from aiogram.fsm.context import FSMContext

order_busket = Router()


@order_busket.callback_query(F.data == "buy_from_busket")
async def check_difference(callback: types.CallbackQuery, state: FSMContext):

    ...