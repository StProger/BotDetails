from config import TOKEN_DIRECTUS, DIRECTUS_API_URL

import aiohttp

from scrap_details import start_parser

import json


class DatabaseAPI(object):

    @staticmethod
    async def user_exist(telegram_id: int):

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_users?filter[telegram_id][_eq]={telegram_id}"
        async with aiohttp.ClientSession(headers=headers) as session:

            response = await session.get(url=url)
            data = await response.json()
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

    @staticmethod
    async def get_about_company():

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_settings?filter[id][_eq]=1"
        async with aiohttp.ClientSession(headers=headers) as session:

            response = await session.get(url=url)
            data = await response.json()
        print(data)
        return data["data"][0]["about_company"]

    @staticmethod
    async def get_refund():

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_settings?filter[id][_eq]=1"
        async with aiohttp.ClientSession(headers=headers) as session:
            response = await session.get(url=url)
            data = await response.json()
        print(data)
        return data["data"][0]["refund_info"]

    @staticmethod
    async def get_data_for_articul(telegram_id, article):

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_settings?filter[id][_eq]=1"
        async with aiohttp.ClientSession(headers=headers) as session:
            response = await session.get(url=url)
            data = await response.json()
        login = data["data"][0]["login"]
        password = data["data"][0]["password"]
        result = start_parser(article=article,
                              username=login,
                              password=password)
        if result is None or result == False:
            return False
        else:
            with open(f"data/{telegram_id}_data.json", "w") as file:

                json.dump(result, file, ensure_ascii=False, indent=4)
            return True

    @staticmethod
    async def get_percent():

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_settings?filter[id][_eq]=1"
        async with aiohttp.ClientSession(headers=headers) as session:
            response = await session.get(url=url)
            data = await response.json()
        return data["data"][0]["percent"]

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
        return data["data"]

    @staticmethod
    async def get_config():

        BEARER_TOKEN = f"Bearer {TOKEN_DIRECTUS}"

        headers = {
            'Authorization': BEARER_TOKEN
        }

        url = f"{DIRECTUS_API_URL}/items/autogait_settings?filter[id][_eq]=1"
        async with aiohttp.ClientSession(headers=headers) as session:
            response = await session.get(url=url)
            data = await response.json()
        return data["data"][0]