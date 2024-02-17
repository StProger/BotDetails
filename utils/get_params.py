from aiogram.fsm.context import FSMContext

from db_api.api import DatabaseAPI

from aiogram import md


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