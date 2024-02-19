import re

from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db_api.api import DatabaseAPI
from keyboard import menu

from db_api.busket.api import Busket

import json

from utils.get_params import get_params, get_params_one_detail, params_select_item
from utils.params_busket import get_price_with_percent

from .get_detail import SGetDetail



busket_router = Router()


class SBusket(StatesGroup):

    order_only = State()
    point_pickup = State()
    contacts = State()
    photo_pay = State()
    note = State()


@busket_router.callback_query(SGetDetail.order, F.data.contains("add_to_busket"))
async def add_item_to_busket(callback: types.CallbackQuery, state: FSMContext):

    count_items = await Busket.count_items(user_id=callback.from_user.id)
    if count_items >= 5:
        await callback.answer("В вашей корзине 5 товаров, добавление невозможно.",
                              show_alert=True)
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
                          user_id=callback.from_user.id,
                          count_item=state_data['count_product'])
    await callback.answer("Товар добавлен в корзину✅", show_alert=True)


@busket_router.callback_query(SGetDetail.order, F.data.contains("minus_item_"))
async def minus_item_busket(callback: types.CallbackQuery, state: FSMContext):
    current_count = int(callback.data.split("_")[-1])
    if current_count == 0:
        await callback.answer()
        return
    else:
        await state.update_data(count_product=current_count)
        state_data = await state.get_data()
        builder = InlineKeyboardBuilder()
        builder.button(text="Добавить в корзину", callback_data=f"add_to_busket_{state_data['index_detail']}")
        builder.row(
            types.InlineKeyboardButton(
                text="➖", callback_data=f"minus_item_{current_count - 1}"
            ),
            types.InlineKeyboardButton(
                text=f"{current_count} шт.", callback_data="_"
            ),
            types.InlineKeyboardButton(
                text="➕", callback_data=f"plus_item_{current_count + 1}"
            )
        )
        builder.row(
            types.InlineKeyboardButton(text="Оформить заказ", callback_data="go_order")
        )
        builder.row(
            types.InlineKeyboardButton(
                text="Назад", callback_data="back_to_choose_detail"
            ),
            types.InlineKeyboardButton(
                text="Меню", callback_data="go_menu"
            )
        )
        builder.row(
            types.InlineKeyboardButton(
                text="Ввести другой артикул", callback_data="get_detail_menu"
            )
        )

        await callback.message.edit_reply_markup(
            text=callback.message.text,
            reply_markup=builder.as_markup()
        )


@busket_router.callback_query(SGetDetail.order, F.data.contains("plus_item_"))
async def minus_item_busket(callback: types.CallbackQuery, state: FSMContext):
    current_count = int(callback.data.split("_")[-1])

    await state.update_data(count_product=current_count)
    state_data = await state.get_data()
    builder = InlineKeyboardBuilder()
    builder.button(text="Добавить в корзину", callback_data=f"add_to_busket_{state_data['index_detail']}")
    builder.row(
        types.InlineKeyboardButton(
            text="➖", callback_data=f"minus_item_{current_count - 1}"
        ),
        types.InlineKeyboardButton(
            text=f"{current_count} шт.", callback_data="_"
        ),
        types.InlineKeyboardButton(
            text="➕", callback_data=f"plus_item_{current_count + 1}"
        )
    )
    builder.row(
        types.InlineKeyboardButton(text="Оформить заказ", callback_data="go_order")
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Назад", callback_data="back_to_choose_detail"
        ),
        types.InlineKeyboardButton(
            text="Меню", callback_data="go_menu"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Ввести другой артикул", callback_data="get_detail_menu"
        )
    )

    await callback.message.edit_reply_markup(
        text=callback.message.text,
        reply_markup=builder.as_markup()
    )


@busket_router.callback_query(F.data.contains("drop_busket_"))
async def delete_item(callback: types.CallbackQuery):

    item_id = callback.data.split("_")[-1]
    await Busket.delete_item(item_id=item_id)
    result = await Busket.get_items(user_id=callback.from_user.id)
    if len(result[2]) != 0:
        text = result[0]
        keyboard = result[1]
        text += "\n\nДля удаления товара из корзины нажмите на название товара снизу⬇️"

        await callback.message.edit_text(
            text=text,
            reply_markup=keyboard
        )
    else:
        builder = InlineKeyboardBuilder()
        builder.button(text="Заказать деталь", callback_data="get_detail_menu")
        builder.button(text="Меню", callback_data="go_menu")
        builder.adjust(1)
        await callback.message.edit_text(
            text="Корзина пуста",
            reply_markup=builder.as_markup()
        )


@busket_router.callback_query(F.data.contains("clean_busket"))
async def delete_item(callback: types.CallbackQuery):

    await Busket.clear_busket(user_id=callback.from_user.id)
    builder = InlineKeyboardBuilder()
    builder.button(text="Заказать деталь", callback_data="get_detail_menu")
    builder.button(text="Меню", callback_data="go_menu")
    builder.adjust(1)
    await callback.message.edit_text(
        text="Корзина очищена",
        reply_markup=builder.as_markup()
    )


@busket_router.callback_query(F.data == "buy_from_busket")
async def get_point(callback: types.CallbackQuery, state: FSMContext):

    warning_text = await DatabaseAPI.get_warning_text()
    if warning_text:
        await state.set_state(SBusket.order_only)
        warning_text = warning_text
        await callback.message.edit_text(
            text=warning_text,
            reply_markup=menu.key_order_busket()
        )
    else:
        await state.set_state(SBusket.point_pickup)
        points = await DatabaseAPI.get_points()
        text = "Выберите пункт самовывоза⬇️"
        await callback.message.edit_text(
            text=text,
            reply_markup=menu.key_points(points=points)
        )


@busket_router.callback_query(SBusket.order_only, F.data=="go_order")
async def get_point(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state(SGetDetail.point_pickup)
    points = await DatabaseAPI.get_points()
    text = "Выберите пункт самовывоза⬇️"
    await callback.message.edit_text(
        text=text,
        reply_markup=menu.key_points(points=points)
    )


@busket_router.callback_query(SBusket.point_pickup)
async def get_contacts(callback: types.CallbackQuery,
                       state: FSMContext):

    id_point = callback.data
    address = await DatabaseAPI.get_adress_point(id_point=id_point)
    await state.update_data(address=address)
    is_phone = await DatabaseAPI.check_phone(user_id=callback.from_user.id)
    if is_phone[0]:
        state_data = await state.get_data()
        await state.update_data(phone=is_phone[1]["phone_number"], name=is_phone[1]["name"])
        card = await DatabaseAPI.get_card()
        await state.set_state(SBusket.photo_pay)
        mes_ = await callback.message.edit_text(
            text=f"Отправьте {state_data['cost_of_busket']} рублей на карту <code>{card}</code> и пришлите скриншот оплаты.",
            reply_markup=menu.key_photo_pay())
        await state.update_data(mes_del=mes_.message_id)
        return
    await state.set_state(SBusket.contacts)
    text = "Отправьте свои контактные данные для связи. Для этого нажмите кнопку ниже⬇️"
    await callback.message.delete()
    mes = await callback.message.answer(
        text=text,
        reply_markup=menu.key_get_contacts()
    )
    await state.update_data(mes_del=mes.message_id)


@busket_router.callback_query(SBusket.contacts)
async def get_photo_pay(message: types.Message,
                        state: FSMContext,
                        bot: Bot):
    contact = message.contact
    await DatabaseAPI.set_contact(phone=contact.phone_number, user_id=message.from_user.id)
    await state.update_data(phone=contact.phone_number, name=contact.first_name)
    state_data = await state.get_data()
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=state_data["mes_del"]
        )
    except:
        pass
    try:
        await message.delete()
    except:
        pass
    card = await DatabaseAPI.get_card()
    await state.set_state(SBusket.photo_pay)
    mes_ = await message.answer(
        f"Отправьте {state_data['cost_of_busket']} рублей на карту <code>{card}</code> и пришлите скриншот оплаты.",
        reply_markup=menu.key_photo_pay())
    await state.update_data(mes_del=mes_.message_id)

    # Остановился на получении фотки