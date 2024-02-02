from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def menu_key():

    builder = InlineKeyboardBuilder()

    builder.button(text="О магазине", callback_data="about_shop")
    builder.button(text="Заказать деталь", callback_data="get_detail_menu")
    builder.button(text="Гарантия и Возврат", callback_data="info_refund")
    builder.adjust(1)
    return builder.as_markup()


def go_menu():

    builder = InlineKeyboardBuilder()

    builder.button(text="Меню", callback_data="go_menu")
    return builder.as_markup()


def choose_producer_key(names: list):

    builder = InlineKeyboardBuilder()
    for i, name in enumerate(names):
        builder.button(text=name, callback_data=str(i))
    builder.adjust(3)
    builder.row(
        InlineKeyboardButton(
            text="Меню", callback_data="go_menu"
        ),
        InlineKeyboardButton(
            text="Ввести другой артикул", callback_data="get_detail_menu"
        )
    )
    return builder.as_markup()


def choose_item_key():

    builder = InlineKeyboardBuilder()
    for i in range(1, 4):
        builder.button(text=str(i), callback_data=str(i-1))
    builder.row(
        InlineKeyboardButton(
            text="Назад", callback_data="back_to_prod"
        ),
        InlineKeyboardButton(
            text="Меню", callback_data="go_menu"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Ввести другой артикул", callback_data="get_detail_menu"
        )
    )
    return builder.as_markup()

