from db_api.api import DatabaseAPI


async def get_params(data: list) -> str:

    official_seller_link = "https://avtopartner.online/bitrix/components/linemedia.auto/search.results/templates/.default/images/ok.gif"
    refund_false_link = "https://avtopartner.online/bitrix/components/linemedia.auto/search.results/templates/.default/images/B_red.gif"
    refund_true_link = "https://avtopartner.online/bitrix/components/linemedia.auto/search.results/templates/.default/images/B_green.gif"
    i3_link = "https://avtopartner.online/bitrix/components/linemedia.auto/search.results/templates/.default/images/i3.gif"
    percent = await DatabaseAPI.get_percent()
    text = ""
    for i, item in enumerate(data):
        refund = False
        official_seller = False

        if any(link in item["Ссылка на метку скалада"] for link in [refund_false_link, i3_link]):
            refund = False
        if official_seller_link in item["Ссылка на метку скалада"]:
            official_seller = True
        if refund_true_link in item["Ссылка на метку скалада"]:
            refund = True
        if official_seller and not any(link in item["Ссылка на метку скалада"] for link in [refund_false_link, i3_link]):
            refund = True
        price_item = int("".join(i for i in item["Цена"].split()[:-1])) * (int(percent)+100/100)
        text += f"{i+1}. {item['Названия']}\n\n" \
                f"<b>АРТИКУЛ</b> - \"{item['Артикул']}\"\n" \
                f"<b>МАРКА</b> - {item['Марка']}\n" \
                f"<b>Цена</b> - {int(price_item)} руб\n" \
                f"<b>Время доставки</b> - {item['Время доставки']}\n"
        if refund:
            text += "<b>ВОЗВРАТ</b> - Возможен\n"
            if official_seller:
                text += "<b>ОФИЦИАЛЬНЫЙ ДИСТРИБЮТОР✅ </b>\n\n"
            else:
                text += "\n"
        else:
            text += "<b>ВОЗВРАТ</b> - Невозможен\n"
            if official_seller:
                text += "<b>ОФИЦИАЛЬНЫЙ ДИСТРИБЮТОР✅ </b>\n\n"
            else:
                text += "\n"
    return text
