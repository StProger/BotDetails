import aiohttp

from config import DIRECTUS_API_URL, TOKEN_DIRECTUS

import json

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


class Busket(object):

    BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

    headers = {
        'Authorization': BEARER_TOKEN
    }

    @classmethod
    async def add_item(cls,
                       item,
                       price,
                       user_id,
                       link_item):
        """
        Добавить элемент в корзину
        :param item:
        :return:
        """

        url = f"{DIRECTUS_API_URL}/items/autogait_cart"
        body = {
            "product": json.dumps(item),
            "user": user_id,
            "price_with_percent": price,
            "title_product": item["Названия"],
            "link_item": link_item
        }
        async with aiohttp.ClientSession(headers=cls.headers) as session:

            response = await session.post(url, json=body)

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

    @classmethod
    async def get_items(cls, user_id):
        """
        Получение предметов из корзины
        :param user_id:
        :return:
        """

        url = f"{DIRECTUS_API_URL}/items/autogait_cart?filter[user][_eq]={user_id}"

        async with aiohttp.ClientSession(headers=cls.headers) as session:
            response = await session.get(url=url)

        if response.status in [200, 204]:
            builder = InlineKeyboardBuilder()
            data = await response.json()
            text = ""
            sum_ = 0
            for item in data["data"]:
                builder.button(text=f"{item['product']['Названия']}", callback_data=f"drop_busket_{item['id']}")
                text += f"{item['product']['Названия']}\n"
                sum_ += int(item["price_with_percent"])
            text += f"\n" \
                    f"Сумма заказа: {sum_} руб."
            builder.adjust(3)
            builder.row(
                InlineKeyboardButton(
                    text="Меню", callback_data="go_menu"
                )
            )
            return text, builder.as_markup()

    @classmethod
    async def is_empty(cls, user_id):
        url = f"{DIRECTUS_API_URL}/items/autogait_cart?filter[user][_eq]={user_id}"

        async with aiohttp.ClientSession(headers=cls.headers) as session:
            response = await session.get(url=url)
        if response.status in [200, 204]:
            data = await response.json()
            if len(data["data"]) == 0:
                return True
            else:
                return False