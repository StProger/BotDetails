from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import requests
import json
from concurrent.futures import ThreadPoolExecutor

import time

def get_attr_from_link(link: str, attr: str) -> str:
    parsed_url = urlparse(link)
    query_params = parse_qs(parsed_url.query)
    attr_str = query_params.get(attr, [None])[0]
    return attr_str


def is_collectable(items: list or None, headers: list) -> tuple | bool:
    if not items: return False
    for item in items:
        if item in headers:
            return True, item
    return False, None


def get_data_by_link(session: requests.Session, link: str) -> list or None:
    data = []
    response = session.post(link)
    if response.status_code in [200]:
        soup = BeautifulSoup(response.text, "html.parser")
        print('ответ получен')
        tables = soup.find_all("h2", {"data-group-id": ["N", "0", "1"]})
        for table in tables:
            is_original = table['data-group-id'] == "N"  # Определяем, является ли таблица для оригинальных запчастей
            trs = table.find_next("table", class_="lm-auto-search-parts").select("tr.hproduct")

            for tr in trs[0:3]:
                data.append({
                    "Названия бренда": get_attr_from_link(link, "brand_title"),
                    "В наличии": tr.select_one("td.instock").text.replace(tr.select_one("td.instock time").text,
                                                                          "").strip("\n").strip(),
                    "Последняя проверка наличия": tr.select_one("td.instock time").text.strip("\n").strip(),
                    "Марка": tr.select_one("td.brand").text.strip("\n").strip(),
                    "Склад": tr.select_one("td.stock").text.strip("\n").strip(),
                    "Ссылка на метку склада": ["https://avtopartner.online" + i.get("src") for i in tr.select("td.stock img")],
                    "Артикул": tr.select_one("td.sku").text.strip("\n").strip(),
                    "Цена": tr.select_one("td.price").text.strip("\n").strip(),
                    "Время доставки": tr.select_one("td.delivery_time").text.strip("\n").strip(),
                    "Бокс": tr.select("td.fn")[0].text.strip("\n").strip(),
                    "Названия": tr.select("td.fn")[1].text.strip("\n").strip(),
                    "Стат. отк.": tr.select_one("div.piechart").text.strip("\n").strip(),
                    "original": is_original
                })

        data = data[0:3]

    return data if data else None


def get_links_by_article(session: requests.Session, article: str) -> list or None:
    response = session.post(f"https://avtopartner.online/auto/search/?q={article}&s=Искать")
    if response.status_code in [200]: 
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.select(".lm-auto-search-result-catalogs .lm-auto-search-catalogs-go a")
        return ["https://avtopartner.online" + link.get("href") for link in links]
    return None


def get_session(username: str, password: str) -> requests.Session or None:
    params = {
        "USER_LOGIN": username, "USER_PASSWORD": password,
        "AUTH_FORM": "Y", "TYPE": "AUTH", "backurl": "/login/"
    }
    session = requests.Session()
    response = session.post("https://avtopartner.online/login/", params=params)
    if response.status_code in [200]: return session
    return None


def get_links(article: str, username: str, password: str) -> dict:
    result = {}
    session = get_session(username, password)
    links = get_links_by_article(session, article)

    for link in links:
        if get_attr_from_link(link, "brand_title") != None:
            result[link] = {"Названия бренда": get_attr_from_link(link, "brand_title")}

    return result


def items(username: str, password: str, link: str) -> dict:
    result = {}
    session = get_session(username, password)
    # print(links)

    data = get_data_by_link(session, link)
    if data: result[link] = data

    return result


def start_parser(article: str, username: str, password: str) -> dict | bool:
    result = {}
    print("Начал искать")
    session = get_session(username, password)
    if session is None:
        return False
    links = get_links_by_article(session, article)
    if links is None or links == [] or links == {}:
        return False

    for link in links:
        data = get_data_by_link(session, link)
        if data: result[link] = data
    return result
if __name__ == '__main__':
    start_time = time.time()
    start_parser(article="ВР22517", username="rmdimin.ar@yandex.ru", password="589348")
    end_time = time.time()
    print(f"Затраченное время: {end_time - start_time}")
# article = "3142025000"
# USERNAME = "rmdimin.ar@yandex.ru"
# PASSWORD = "589348"
#
# result = start_parser(article, USERNAME, PASSWORD)
#
# with open('avtopartner-parser/data.json', 'w', encoding='utf-8') as f:
#     json.dump(result, f, ensure_ascii=False, indent=4)
