import aiohttp
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiohttp import ClientTimeout

from config import DIRECTUS_API_URL, TOKEN_DIRECTUS

import json

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from db_api.api import DatabaseAPI
from scrap_details import items as update_item


class Busket(object):

    BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

    headers = {
        'Authorization': BEARER_TOKEN,
    }

    @classmethod
    async def add_item(cls,
                       item,
                       price,
                       user_id,
                       link_item,
                       count_item):
        """
        Добавить элемент в корзину
        :param item:
        :return:
        """

        url = f"{DIRECTUS_API_URL}/items/autogait_cart"
        body = {
            "product": json.dumps(item),
            "user": user_id,
            "price_with_percent": price * count_item,
            "title_product": item["Названия"],
            "link_item": link_item,
            "count_item": count_item
        }
        async with aiohttp.ClientSession(headers=cls.headers) as session:

            response = await session.post(url, json=body)
            data = await response.json()
            await session.close()
            print(data)

    @classmethod
    async def delete_item(cls, item_id):
        """
        Удалить элемент из корзины
        :param item_id:
        :return:
        """

        url = f"{DIRECTUS_API_URL}/items/autogait_cart/{item_id}"

        async with aiohttp.ClientSession(headers=cls.headers) as session:

            await session.delete(url=url)
            await session.close()

    @classmethod
    async def get_items(cls, user_id, state: FSMContext):
        """
        Получение предметов из корзины
        :param user_id:
        :return:
        """

        url = f"{DIRECTUS_API_URL}/items/autogait_cart?filter[user][_eq]={user_id}"

        async with aiohttp.ClientSession(headers=cls.headers, timeout=ClientTimeout(5)) as session:
            response = await session.get(url=url)
            print(response.status)
            if response.status in [200, 204]:
                print("wgwg")
                builder = InlineKeyboardBuilder()
                print(await response.text())
                data = await response.json()
                print(data)
                text = ""
                sum_ = 0
                for index, item in enumerate(data["data"]):
                    builder.button(text=f"{index + 1}", callback_data=f"drop_busket_{item['id']}")
                    text += f"{index+1}. {item['product']['Названия']} {item['count_item']} шт.\n"
                    sum_ += int(item["price_with_percent"])
                await state.update_data(cost_of_busket=sum_)
                text += f"\n" \
                        f"Сумма заказа: {sum_} руб."
                builder.adjust(3)
                builder.row(
                    InlineKeyboardButton(
                        text="Оформить заказ", callback_data="buy_from_busket"
                    ),
                    InlineKeyboardButton(
                        text="Очистить корзину", callback_data="clean_busket"
                    )
                )
                builder.row(
                    InlineKeyboardButton(
                        text="Меню", callback_data="go_menu"
                    )
                )
                return text, builder.as_markup(), data["data"]

    @classmethod
    async def is_empty(cls, user_id):
        url = f"{DIRECTUS_API_URL}/items/autogait_cart?filter[user][_eq]={user_id}"

        async with aiohttp.ClientSession(headers=cls.headers, timeout=ClientTimeout(10)) as session:
            response = await session.get(url=url)
            if response.status in [200, 204]:
                data = await response.json()
                if len(data["data"]) == 0:

                    return True
                else:

                    return False

    @classmethod
    async def clear_busket(cls, user_id):

        url = f"{DIRECTUS_API_URL}/items/autogait_cart?filter[user][_eq]={user_id}"

        async with aiohttp.ClientSession(headers=cls.headers) as session:
            response = await session.get(url=url)
            data = await response.json()

            for item in data["data"]:
                url = f"{DIRECTUS_API_URL}/items/autogait_cart/{item['id']}"
                await session.delete(url=url)
            await session.close()

    @classmethod
    async def count_items(cls, user_id):

        url = f"{DIRECTUS_API_URL}/items/autogait_cart?filter[user][_eq]={user_id}"

        async with aiohttp.ClientSession(headers=cls.headers) as session:
            response = await session.get(url=url)
            data = await response.json()
            await session.close()
        return len(data["data"])

    @classmethod
    async def check_updates(cls, user_id, state: FSMContext):

        list_for_delete = []

        url = f"{DIRECTUS_API_URL}/items/autogait_cart?filter[user][_eq]={user_id}"
        state_data = await state.get_data()
        async with aiohttp.ClientSession(headers=cls.headers) as session:

            response = await session.get(url=url)
            data = await response.json()
            url_login = f"{DIRECTUS_API_URL}/items/autogait_settings?filter[key][_eq]=login"
            response = await session.get(url=url_login)
            data_ = await response.json()
            login = data_["data"][0]["value"]
            url_password = f"{DIRECTUS_API_URL}/items/autogait_settings?filter[key][_eq]=password"

            response = await session.get(url=url_password)
            data_ = await response.json()
            password = data_["data"][0]["value"]
            await session.close()
        text = ""
        percent = await DatabaseAPI.get_percent()
        for item in data["data"]:

            result = update_item(username=login,
                                 password=password,
                                 link=item["link_item"])
            found = False
            for sub_item in result[item["link_item"]]:
                if item["product"]["Артикул"] == sub_item["Артикул"] and \
                        item["product"]["Названия"] == sub_item["Названия"] and \
                        item["product"]["Марка"] == sub_item["Марка"] and \
                        item["product"]["Склад"] == sub_item["Склад"] and \
                        item["product"]["original"] == sub_item["original"]:
                    found = True
                    if int(sub_item["В наличии"]) == 0:
                        text += f"Товара {item['product']['Названия']} нет в наличии\n"
                        # Сделать логику удаленяи товара
                        list_for_delete.append(item["id"])

                    elif int(sub_item["В наличии"]) < item["count_item"]:
                        text += f"Товара {item['product']['Названия']} недостаточно на складе\n"
                        list_for_delete.append(item['id'])

                    else:
                        # Проверяем изменение цены
                        price_item = float("".join(i for i in sub_item["Цена"].split()[:-1])) * ((float(percent) + 100) / 100)
                        if int(price_item) * item['count_item'] != int(item["price_with_percent"]):

                            text += f"Общая цена за {item['product']['Названия']} изменилась с {int(item['price_with_percent'])} " \
                                    f"на {int(price_item) * item['count_item']}\n"
                            # Сделать логику изменения цены товара в бд
                            print("Обновляю цену")
                            await cls.update_price(item_id=item['id'], price=price_item*item['count_item'])
                            cost_order = state_data["cost_of_busket"]
                            print(f"Old: {cost_order}")
                            cost_order += (int(price_item) * int(item['count_item'])) - int(item["price_with_percent"])
                            print(f"New: {cost_order}")
                            await state.update_data(cost_of_busket=cost_order)
                if found:
                    break
        if text == "":
            return text
        else:
            await state.update_data(list_for_delete=list_for_delete)
            return text

    @classmethod
    async def get_products(cls, user_id):

        url = f"{DIRECTUS_API_URL}/items/autogait_cart?filter[user][_eq]={user_id}"

        async with aiohttp.ClientSession(headers=cls.headers, timeout=aiohttp.ClientTimeout(10)) as session:
            response = await session.get(url=url)

            if response.status in [200, 204]:
                data = await response.json()
                return data["data"]
            else:
                await Busket.get_products(user_id=user_id)

    @classmethod
    async def add_order_to_db(cls, user_id, state_data: dict, bot: Bot, text):

        for link in state_data["links_buket"]:
            text.replace("<b>", " ").replace("</b>", " ").replace(
                f"<b>Ссылка</b> - <a href='{link}'>Товар</a>", "", 1)
        body = {
            "user": user_id,
            "product": text,
            "note": state_data.get("note", ""),
            "no_percent_price": state_data["old_price"],
            "percent_price": state_data["price_detail"],
            "profit_sum": int(state_data["price_detail"] - state_data["old_price"]),
            "approved": False,
            "link_item": ", ".join(state_data["links_buket"])
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_orders"
        async with aiohttp.ClientSession(headers=cls.headers) as session:
            response = await session.post(url=url, json=body)
            data = await response.json()
            await session.close()
        print(f"Данные о добавлении заказа: {data}")
            # await bot.send_message(
            #     chat_id=1878562358,
            #     text=str(data)
            # )
        try:
            return data["data"]
        except Exception as ex:
            print(f"Ошибка: {ex}")
        await session.close()

    @classmethod
    async def update_price(cls, item_id, price):
        print(price)
        url = f"{DIRECTUS_API_URL}/items/autogait_cart/{item_id}"
        body = {
            "price_with_percent": price
        }
        async with aiohttp.ClientSession(headers=cls.headers) as session:
            response = await session.patch(url=url, json=body)
            print(await response.json())
            await session.close()







