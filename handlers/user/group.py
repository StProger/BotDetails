from aiogram import Router, F, types, Bot

from db_api.api import DatabaseAPI

import re

from keyboard import menu


grorup_router = Router()


@grorup_router.message()
async def set_number_order(message: types.Message, bot: Bot):

    have_basket = False
    if message.reply_to_message.text is not None:
        have_basket = True


    if not message.reply_to_message:
        return
    else:
        if not have_basket:
            if "НОМЕР ЗАКАЗА С САЙТА" in message.reply_to_message.text:
                await message.reply("Данному заказу уже присвоен номер.")
                return
            number_order = message.text
            # order_id_message = message.reply_to_message.message_id
            url_message = message.reply_to_message.message_id
            group_id = await DatabaseAPI.get_channel_id()
            #  = f"https://t.me/c/{group_id}/{message.message_id}"
            order = await DatabaseAPI.get_order_by_url(url=url_message)
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
            await message.reply_to_message.edit_text(text=f"{text}\n\nНОМЕР ЗАКАЗА С САЙТА: {number_order}",
                                                     reply_markup=menu.key_after_set_number(user_id=user_id,
                                                                                               order_id=order_id,
                                                                                               caption=text),
                                                     disable_web_page_preview=True)
        else:
            if "НОМЕР ЗАКАЗА С САЙТА" in message.reply_to_message.text:
                await message.reply("Данному заказу уже присвоен номер.")
                return
            number_order = message.text
            url_message = message.reply_to_message.message_id

            # group_id = await DatabaseAPI.get_channel_id()
            order = await DatabaseAPI.get_order_by_url(url=url_message)
            # link_item = order["link_item"]

            order_id = order["id"]
            user_id = order["user"]
            await DatabaseAPI.update_order_number(order_number=number_order,
                                                  order_id=order_id)
            print("Добавил номер заказа с сайта")
            text = message.reply_to_message.text
            pattern = re.compile(r'Пункт самовывоза.*?Клиент', re.DOTALL)
            point_ = re.search(pattern, text).group(0).replace("Клиент", "").strip()
            for link in order["link_item"].split(","):
                text = text.replace("Ссылка - Товар", f"Ссылка - <a href='{link.strip()}'>Товар</a>", 1).lstrip()
                print(text)
            # print(text)
            text_ = f"<b>ВАШ НОМЕР ЗАКАЗА {number_order}</b>\n\n"
            # print(result)
            pattern = re.compile(r'ТОВАР.*?Склад', re.DOTALL)
            result = ""
            results = re.findall(pattern, text)
            for result_ in results:
                result += result_.replace("Склад", "") + "\n"
            text_ += result
            text_ += f"\n{point_}"

            await bot.send_message(
                chat_id=user_id,
                text=text_,
                reply_markup=menu.key_menu_after_success()
            )
            await message.reply_to_message.edit_text(text=f"{text}\n\nНОМЕР ЗАКАЗА С САЙТА: {number_order}",
                                                     reply_markup=menu.key_after_set_number_basket(user_id=user_id,
                                                                                                      order_id=order_id,
                                                                                                      caption=text),
                                                     disable_web_page_preview=True)


