import aiohttp

from config import DIRECTUS_API_URL, TOKEN_DIRECTUS


class Busket(object):

    BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

    headers = {
        'Authorization': BEARER_TOKEN
    }

    @classmethod
    async def add_item(cls, item):
        """
        Добавить элемент в корзину
        :param item:
        :return:
        """

        url = f"{DIRECTUS_API_URL}/items/autogait_cart"
        body = {
            "item": item
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

        url = f"{DIRECTUS_API_URL}/items/autogait_cart?filter[telegram_id][_eq]={user_id}"

        async with aiohttp.ClientSession(headers=cls.headers) as session:
            response = await session.get(url=url)


        if response.status in [200, 204]:
            data = await response.json()
            return data["data"]