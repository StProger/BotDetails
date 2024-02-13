from aiogram import Router, F, types, Bot

from db_api.api import DatabaseAPI

import re

from keyboard import menu


grorup_router = Router()


@grorup_router.message()
async def set_number_order(message: types.Message, bot: Bot):


    if not message.reply_to_message:
        return
    else:
        if "НОМЕР ЗАКАЗА С САЙТА" in message.reply_to_message.caption:
            await message.answer("Данному заказу уже присвоен номер.")
            return
        number_order = message.text
        # order_id_message = message.reply_to_message.message_id
        url_message = message.reply_to_message.get_url()
        group_id = await DatabaseAPI.get_channel_id()
        link_message = f"https://t.me/c/{group_id}/{message.message_id}"
        order = await DatabaseAPI.get_order_by_url(url=link_message)
        link_item = order["link_item"]
        order_id = order["id"]
        user_id = order["user"]
        await DatabaseAPI.update_order_number(order_number=number_order,
                                              order_id=order_id)
        print("Добавил номер заказа с сайта")
        text = message.reply_to_message.caption.replace("Ссылка - Товар", f"Ссылка - <a href='{link_item}'>Товар</a>")
        pattern = re.compile(r'Товар.*?Склад', re.DOTALL)
        text_ = f"<b>ВАШ НОМЕР ЗАКАЗА {number_order}</b>\n\n"
        result = re.search(pattern, text).group(0).replace("Склад", "").strip()
        text_ += result
        await bot.send_message(
            chat_id=user_id,
            text=text_,
            reply_markup=menu.key_menu_after_success()
        )
        await message.reply_to_message.edit_caption(caption=f"{text}\n\nНОМЕР ЗАКАЗА С САЙТА: {number_order}",
                                                    reply_markup=menu.key_after_set_number(user_id=user_id,
                                                                                           order_id=order_id,
                                                                                           caption=text))

