from config import URL_UPDATE

import aiohttp


async def sent_update_leadtech(body):

    url = URL_UPDATE

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(10)) as session:
        response = await session.post(url, json=body)
    print("Отправил апдейт")
    print(response.status)