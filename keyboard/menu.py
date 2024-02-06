from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton


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
        builder.button(text=str(i), callback_data=f"{str(i - 1)}")
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


def key_order():
    builder = InlineKeyboardBuilder()
    builder.button(text="Оформить заказ", callback_data="go_order")
    builder.row(
        InlineKeyboardButton(
            text="Назад", callback_data="back_to_choose_detail"
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


def key_points(points):

    builder = InlineKeyboardBuilder()

    for point in points:
        builder.button(text=point["button_name"], callback_data=str(point["id"]))
    builder.adjust(3)
    builder.row(
        InlineKeyboardButton(
            text="Назад", callback_data="back_to_choose_detail"
        ),
        InlineKeyboardButton(
            text="Меню", callback_data="go_menu"
        )
    )


def key_get_contacts():

    builder = ReplyKeyboardBuilder()
    builder.button(text="Отправить свой контакт📲", request_contact=True)
    keyboard = builder.as_markup()
    keyboard.resize_keyboard = True
    keyboard.one_time_keyboard = True
    return keyboard

