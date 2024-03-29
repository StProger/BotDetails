from aiogram import Bot

from config import TOKEN_DIRECTUS, DIRECTUS_API_URL

import aiohttp

from scrap_details import start_parser, get_links, items

import json


class DatabaseAPI(object):

    @staticmethod
    async def user_exist(telegram_id: int):

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }
        print(headers)

        url = f"{DIRECTUS_API_URL}/items/autogait_users?filter[telegram_id][_eq]={telegram_id}"
        async with aiohttp.ClientSession(headers=headers) as session:

            response = await session.get(url=url)
            data = await response.json()
            await session.close()
        print(data)

        if len(data["data"]) == 0:
            return False
        else:
            return True

    @staticmethod
    async def register_user(telegram_id: int, username: str, name: str):

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_users"
        body = {
            "telegram_id": telegram_id,
            "username": f"@{username}",
            "name": name
        }

        async with aiohttp.ClientSession(headers=headers) as session:

            await session.post(url=url, json=body)
            await session.close()

    @staticmethod
    async def get_about_company():

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_settings?filter[key][_eq]=about_company"
        async with aiohttp.ClientSession(headers=headers) as session:

            response = await session.get(url=url)
            data = await response.json()
            await session.close()
        print(data)
        return data["data"][0]["value"]

    @staticmethod
    async def get_refund():

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_settings?filter[key][_eq]=refund_info"
        async with aiohttp.ClientSession(headers=headers) as session:
            response = await session.get(url=url)
            data = await response.json()
            await session.close()
        print(data)
        return data["data"][0]["value"]

    @staticmethod
    async def get_links(article, telegram_id):

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url_login = f"{DIRECTUS_API_URL}/items/autogait_settings?filter[key][_eq]=login"
        async with aiohttp.ClientSession(headers=headers) as session:
            response = await session.get(url=url_login)
            data = await response.json()
            login = data["data"][0]["value"]
            url_password = f"{DIRECTUS_API_URL}/items/autogait_settings?filter[key][_eq]=password"

            response = await session.get(url=url_password)
            data = await response.json()
            password = data["data"][0]["value"]
            await session.close()
        links = get_links(article=article, username=login, password=password)
        if links is None or links == {}:
            data_link = await DatabaseAPI.get_data_by_link(link=f"https://avtopartner.online/auto/search/?q={article}&s=%D0%98%D1%81%D0%BA%D0%B0%D1%82%D1%8C", telegram_id=telegram_id)
            if not data_link:
                return False
            else:
                return True
        else:
            with open(f"data/{telegram_id}_data_links.json", "w") as file:
                json.dump(links, file, ensure_ascii=False, indent=4)
            return True

    @staticmethod
    async def get_data_by_link(telegram_id, link):

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url_login = f"{DIRECTUS_API_URL}/items/autogait_settings?filter[key][_eq]=login"
        async with aiohttp.ClientSession(headers=headers) as session:
            response = await session.get(url=url_login)
            data = await response.json()
            login = data["data"][0]["value"]
            url_password = f"{DIRECTUS_API_URL}/items/autogait_settings?filter[key][_eq]=password"
            response = await session.get(url=url_password)
            data = await response.json()
            password = data["data"][0]["value"]
            await session.close()
        result = items(username=login, password=password, link=link)
        if result == {}:
            return False
        with open(f"data/{telegram_id}_data.json", "w") as file:
            json.dump(result, file, ensure_ascii=False, indent=4)
        return True

    @staticmethod
    async def get_percent():

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_settings?filter[key][_eq]=percent"
        async with aiohttp.ClientSession(headers=headers) as session:
            response = await session.get(url=url)
            data = await response.json()
            await session.close()
        return data["data"][0]["value"]

    @staticmethod
    async def get_points():

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_pickup_points"

        async with aiohttp.ClientSession(headers=headers) as session:
            response = await session.get(url=url)
            data = await response.json()
            await session.close()
        return data["data"]

    @staticmethod
    async def get_warning_text():

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_settings?filter[key][_eq]=warning_text"
        async with aiohttp.ClientSession(headers=headers) as session:
            response = await session.get(url=url)
            data = await response.json()
            await session.close()
        return data["data"][0]["value"]

    @staticmethod
    async def get_card():

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_settings?filter[key][_eq]=card"
        async with aiohttp.ClientSession(headers=headers) as session:
            response = await session.get(url=url)
            data = await response.json()
            await session.close()
        return data["data"][0]["value"]

    @staticmethod
    async def get_channel_id():

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_settings?filter[key][_eq]=group"
        async with aiohttp.ClientSession(headers=headers) as session:
            response = await session.get(url=url)
            data = await response.json()
            await session.close()
        return data["data"][0]["value"]

    @staticmethod
    async def add_order_to_db(user_id, state_data: dict, bot: Bot):

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }
        body = {
            "user": user_id,
            "product": state_data["choosed_detail"].replace("<b>", " ").replace("</b>", " ").replace(f"<b>Ссылка</b> - <a href='{state_data['choosed_producer']}'>Товар</a>", ""),
            "note": state_data.get("note", ""),
            "no_percent_price": state_data["old_price"],
            "percent_price": state_data["price_detail"],
            "profit_sum": int(state_data["price_detail"] - state_data["old_price"]),
            "approved": False,
            "link_item": state_data["choosed_producer"]
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_orders"
        async with aiohttp.ClientSession(headers=headers) as session:
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

    @staticmethod
    async def update_url_order(id_order, link):

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }
        body = {
            "order_link": link
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_orders/{id_order}"
        async with aiohttp.ClientSession(headers=headers) as session:
            await session.patch(url=url, json=body)
            await session.close()

    @staticmethod
    async def set_contact(phone, user_id):

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }
        body = {
            "phone_number": phone
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_users/{user_id}"
        async with aiohttp.ClientSession(headers=headers) as session:
            await session.patch(url=url, json=body)

    @staticmethod
    async def check_phone(user_id):

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_users?filter[telegram_id][_eq]={user_id}"
        async with aiohttp.ClientSession(headers=headers) as session:
            result = await session.get(url=url)
            data = await result.json()
        if data["data"][0]["phone_number"]:
            return True, data["data"][0]
        else:
            return (False, )

    @staticmethod
    async def update_approve(id_order):

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }
        body = {
            "approved": True
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_orders/{id_order}"
        async with aiohttp.ClientSession(headers=headers) as session:
            await session.patch(url=url, json=body)

    @staticmethod
    async def get_adress_point(id_point):

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_pickup_points?filter[id][_eq]={id_point}"

        async with aiohttp.ClientSession(headers=headers) as session:
            response = await session.get(url=url)
            data = await response.json()
        return data["data"][0]["address"]

    @staticmethod
    async def get_days():

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_settings?filter[key][_eq]=allowance_days"
        async with aiohttp.ClientSession(headers=headers) as session:
            response = await session.get(url=url)
            data = await response.json()
        return data["data"][0]["value"]

    @staticmethod
    async def get_order_by_url(url):

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_orders?filter[order_link][_eq]={url}"
        async with aiohttp.ClientSession(headers=headers) as session:
            response = await session.get(url=url)
            data = await response.json()
        return data["data"][0]

    @staticmethod
    async def update_order_number(order_number, order_id):

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }
        body = {
            "order_number": order_number
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_orders/{order_id}"
        async with aiohttp.ClientSession(headers=headers) as session:
            await session.patch(url=url, json=body)

    @staticmethod
    async def get_instruction():

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_settings?filter[key][_eq]=instruction"
        async with aiohttp.ClientSession(headers=headers) as session:
            response = await session.get(url=url)
            data = await response.json()
        return data["data"][0]["value"]

    @staticmethod
    async def get_order_number(order_link):

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_orders?filter[order_link][_eq]={order_link}"
        async with aiohttp.ClientSession(headers=headers) as session:

            response = await session.get(url=url)
            data = await response.json()
            # print(data)
        return data["data"][0]["order_number"]


    @staticmethod
    async def insert_hash(item, link_item, hash):

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }
        body = {
            "product": item,
            "link_item": link_item,
            "hash": hash
        }
        url = f"{DIRECTUS_API_URL}/items/autogait_hashs"
        async with aiohttp.ClientSession(headers=headers) as session:
            response = await session.post(url=url, json=body)

    @staticmethod
    async def get_hash_data(hash_):

        url = f"{DIRECTUS_API_URL}/items/autogait_hashs?filter[hash][_eq]={hash_}"
        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        async with aiohttp.ClientSession(headers=headers) as session:

            response = await session.get(url=url)

        data = await response.json(content_type=None)

        return data["data"][0]

    @staticmethod
    async def get_admins():

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_users?filter[admin][_eq]=True"

        async with aiohttp.ClientSession(headers=headers) as session:

            response = await session.get(url=url)

        if response.status in [200, 204]:

            data = await response.json(content_type=None)
            return [int(user["telegram_id"]) for user in data["data"]]

        else:
            return []

