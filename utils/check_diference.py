from bs4 import BeautifulSoup

from scrap_details import get_session

import re


def get_availability_and_price(link: str,
                               product_id: str,
                               username: str,
                               password: str) -> dict:
    group_ids = ["N", "0", "1"]
    session = get_session(username,
                          password)  # Убедитесь, что функция get_session правильно определена и возвращает объект сессии
    response = session.post(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Поиск таблиц по группам идентификаторов
        tables = soup.find_all("h2", {"data-group-id": group_ids})
        for table in tables:
            trs = table.find_next("table", class_="lm-auto-search-parts").select("tr.hproduct")
            for tr in trs:
                buy_button = tr.select_one("a.btn.btn-mini")
                if buy_button:
                    onclick_text = buy_button.get('onclick', '')
                    # Поиск хэша
                    hash_match = re.search(r"extra%5Bhash%5D=([\da-fA-F]+)", onclick_text)
                    # Попытка найти part_id и supplier_id, если хэш не найден
                    part_id_match = re.search(r"part_id=(\d+)", onclick_text)
                    supplier_id_match = re.search(r"supplier_id=(\d+)", onclick_text)

                    # Составление идентификатора на основе доступной информации
                    if hash_match:
                        current_id = hash_match.group(1)
                    elif part_id_match and supplier_id_match:
                        current_id = f"part_id: {part_id_match.group(1)}, supplier_id: {supplier_id_match.group(1)}"
                    else:
                        current_id = 'Недоступно'
                    print(current_id)
                    if current_id == product_id:
                        availability = tr.select_one("td.instock").text.replace(tr.select_one("td.instock time").text,
                                                                                "").strip("\n").strip()
                        price = tr.select_one("td.price").text.strip("\n").strip()
                        return {"availability": availability, "price": price}

    # Если товар не найден в указанных таблицах, возвращаем значения, указывающие на отсутствие товара
    return {"availability": None, "price": None}