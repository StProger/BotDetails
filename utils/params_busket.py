import aiohttp

from config import DIRECTUS_API_URL, TOKEN_DIRECTUS

from db_api.api import DatabaseAPI


async def get_price_with_percent(item):

    percent = await DatabaseAPI.get_percent()
    price_item = float("".join(i for i in item["Цена"].split()[:-1])) * ((float(percent) + 100) / 100)
    return int(price_item)