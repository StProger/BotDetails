from aiogram.fsm.context import FSMContext

from db_api.api import DatabaseAPI

from aiogram import md

from db_api.busket.api import Busket


async def get_params(data: list) -> str:
    print(data)

    official_seller_link = "https://avtopartner.online/bitrix/components/linemedia.auto/search.results/templates/.default/images/ok.gif"
    # refund_false_link = "https://avtopartner.online/bitrix/components/linemedia.auto/search.results/templates/.default/images/B_red.gif"
    # refund_true_link = "https://avtopartner.online/bitrix/components/linemedia.auto/search.results/templates/.default/images/B_green.gif"
    # i3_link = "https://avtopartner.online/bitrix/components/linemedia.auto/search.results/templates/.default/images/i3.gif"
    percent = await DatabaseAPI.get_percent()
    days = int(await DatabaseAPI.get_days())
    text = ""
    for i, item in enumerate(data):
        # refund = False
        official_seller = False

        # if any(link in item["Ссылка на метку склада"] for link in [refund_false_link, i3_link]):
        #     refund = False
        if official_seller_link in item["Ссылка на метку склада"]:
            official_seller = True
        # if refund_true_link in item["Ссылка на метку склада"]:
        #     refund = True
        # if official_seller and not any(link in item["Ссылка на метку склада"] for link in [refund_false_link, i3_link]):
        #     refund = True
        price_item = float("".join(i for i in item["Цена"].split()[:-1])) * ((float(percent)+100)/100)
        text += f"{i+1}. {item['Названия']}\n\n" \
                f"<b>АРТИКУЛ</b> - \"{item['Артикул']}\"\n" \
                f"<b>МАРКА</b> - {item['Марка']}\n" \
                f"<b>Цена</b> - {int(price_item)} руб\n" \
                f"<b>Время доставки</b> - {int(item['Время доставки'].split()[0]) + days} д.\n"

        #text += "<b>ВОЗВРАТ</b> - Возможен\n"
        if official_seller:
            text += "<b>ОФИЦИАЛЬНЫЙ ДИСТРИБЮТОР✅ </b>\n"
        if not (item["original"]):
            text += "<b>НЕОРИГИНАЛЬНЫЙ АНАЛОГ</b>\n"
        text += "\n"

    return text


async def get_params_one_detail(item, state: FSMContext, link, adress):

    official_seller_link = "https://avtopartner.online/bitrix/components/linemedia.auto/search.results/templates/.default/images/ok.gif"
    # refund_false_link = "https://avtopartner.online/bitrix/components/linemedia.auto/search.results/templates/.default/images/B_red.gif"
    # refund_true_link = "https://avtopartner.online/bitrix/components/linemedia.auto/search.results/templates/.default/images/B_green.gif"
    # i3_link = "https://avtopartner.online/bitrix/components/linemedia.auto/search.results/templates/.default/images/i3.gif"
    percent = await DatabaseAPI.get_percent()
    text = ""
    # refund = False
    official_seller = False
    days = int(await DatabaseAPI.get_days())

    # if any(link in item["Ссылка на метку склада"] for link in [refund_false_link, i3_link]):
    #     refund = False
    if official_seller_link in item["Ссылка на метку склада"]:
        official_seller = True
    # if refund_true_link in item["Ссылка на метку склада"]:
    #     refund = True
    # if official_seller and not any(link in item["Ссылка на метку склада"] for link in [refund_false_link, i3_link]):
    #     refund = True
    old_price = int("".join(i for i in item["Цена"].split()[:-1]))
    price_item = float("".join(i for i in item["Цена"].split()[:-1])) * ((float(percent) + 100) / 100)
    await state.update_data(price_detail=int(price_item), old_price=old_price)
    text += f"Товар: {item['Названия']}\n\n" \
            f"<b>АРТИКУЛ</b> - \"{item['Артикул']}\"\n" \
            f"<b>МАРКА</b> - {item['Марка']}\n" \
            f"<b>Цена</b> - {int(price_item)} руб\n" \
            f"<b>Время доставки</b> - {int(item['Время доставки'].split()[0]) + days} д.\n" \
            f"<b>Пункт самовывоза</b> - {adress}\n"

    # text += "<b>ВОЗВРАТ</b> - Возможен\n"
    if official_seller:
        text += "<b>ОФИЦИАЛЬНЫЙ ДИСТРИБЮТОР✅ </b>\n"
    if not (item["original"]):
        text += "<b>НЕОРИГИНАЛЬНЫЙ АНАЛОГ</b>\n"

    text += f"<b>Склад</b> - {item['Склад']}\n"
    text += f"<b>Ссылка</b> - <a href='{link}'>Товар</a>\n"
    return text


async def params_select_item(item, state: FSMContext):

    official_seller_link = "https://avtopartner.online/bitrix/components/linemedia.auto/search.results/templates/.default/images/ok.gif"
    percent = await DatabaseAPI.get_percent()
    days = int(await DatabaseAPI.get_days())
    text = ""
    official_seller = False

    if official_seller_link in item["Ссылка на метку склада"]:
        official_seller = True
    old_price = int("".join(i for i in item["Цена"].split()[:-1]))
    price_item = float("".join(i for i in item["Цена"].split()[:-1])) * ((float(percent) + 100) / 100)
    await state.update_data(price_detail=int(price_item), old_price=old_price)
    text += f"{item['Названия']}\n\n" \
            f"<b>АРТИКУЛ</b> - \"{item['Артикул']}\"\n" \
            f"<b>МАРКА</b> - {item['Марка']}\n" \
            f"<b>Цена</b> - {int(price_item)} руб\n" \
            f"<b>Время доставки</b> - {int(item['Время доставки'].split()[0]) + days} д.\n"

    if official_seller:
        text += "<b>ОФИЦИАЛЬНЫЙ ДИСТРИБЮТОР✅ </b>\n"
    if not (item["original"]):
        text += "<b>НЕОРИГИНАЛЬНЫЙ АНАЛОГ</b>\n"
    text += "\n"

    return text


async def get_params_busket(user_id, state: FSMContext):

    state_data = await state.get_data()
    products = await Busket.get_products(user_id=user_id)
    old_sum = 0
    sum_ = 0
    text = ""
    links = []
    for item in products:
        official_seller_link = "https://avtopartner.online/bitrix/components/linemedia.auto/search.results/templates/.default/images/ok.gif"
        links.append(item["link_item"])
        official_seller = False
        days = int(await DatabaseAPI.get_days())

        if official_seller_link in item["Ссылка на метку склада"]:
            official_seller = True

        old_price = int("".join(i for i in item['product']["Цена"].split()[:-1]))
        old_sum += old_price
        sum_ += int(item["price_with_percent"])

        text += f"Товар: {item['Названия']}\n\n" \
                f"<b>АРТИКУЛ</b> - \"{item['product']['Артикул']}\"\n" \
                f"<b>МАРКА</b> - {item['product']['Марка']}\n" \
                f"<b>Цена</b> - {int(item['price_with_percent'])} руб\n" \
                f"<b>Время доставки</b> - {int(item['product']['Время доставки'].split()[0]) + days} д.\n" \
                f"<b>Кол-во</b> - {item['count_item']} шт.\n"

        if official_seller:
            text += "<b>ОФИЦИАЛЬНЫЙ ДИСТРИБЮТОР✅ </b>\n"
        if not (item['product']["original"]):
            text += "<b>НЕОРИГИНАЛЬНЫЙ АНАЛОГ</b>\n"

        text += f"<b>Склад</b> - {item['product']['Склад']}\n"
        text += f"<b>Ссылка</b> - <a href='{item['link_item']}'>Товар</a>\n"

    text = f"<b>Пункт самовывоза</b> - {state_data['address']}\n\n"


    await state.update_data(old_price=old_sum, price_detail=sum_, links_buket=links)
    return text
