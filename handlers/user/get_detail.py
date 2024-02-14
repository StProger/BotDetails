import re

from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import md

from keyboard import menu

from db_api.api import DatabaseAPI

import json

from utils.get_params import get_params, get_params_one_detail


detail_router = Router()


class SGetDetail(StatesGroup):

    article = State()
    choose_producer = State()
    choose_item = State()
    order = State()
    point_pickup = State()
    contacts = State()
    photo_pay = State()
    note = State()


@detail_router.callback_query(F.data == "get_detail_menu")
async def get_article(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state(SGetDetail.article)
    await callback.message.delete()
    mes_ = await callback.message.answer("Отправьте артикул желаемой детали.",
                                  reply_markup=menu.go_menu())
    await state.update_data(mes_del=mes_.message_id)


@detail_router.message(SGetDetail.article)
async def get_producer(message: types.Message, state: FSMContext, bot: Bot):

    state_data = await state.get_data()
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=state_data["mes_del"]
        )
    except:
        pass
    clock_message = await message.answer("Идет поиск товара, подождите немного⏳")
    result = await DatabaseAPI.get_links(article=message.text, telegram_id=message.from_user.id)
    if not result:
        await message.delete()
        await clock_message.delete()
        await message.answer("Нет деталей с таким артикулом, попробуйте другой артикул.",
                             reply_markup=menu.go_menu())
        return

    else:
        with open(f"data/{message.from_user.id}_data_links.json", "r") as file:
            data = json.loads(file.read())

        names = []
        for key in data.keys():
            names.append(data[key]["Названия бренда"])
        await clock_message.delete()
        await message.delete()
        await message.answer(
            text="Выберите производителя",
            reply_markup=menu.choose_producer_key(names=names)
        )
        await state.set_state(SGetDetail.choose_producer)


@detail_router.callback_query(SGetDetail.choose_producer)
async def choose_detail(callback: types.CallbackQuery, state: FSMContext):

    with open(f"data/{callback.from_user.id}_data_links.json", "r") as file:
        data = json.loads(file.read())
    choosed_producer = None
    for i, key in enumerate(data.keys()):
        if i == int(callback.data):
            choosed_producer = key
            break
    print(choosed_producer)
    await DatabaseAPI.get_data_by_link(telegram_id=callback.from_user.id, link=choosed_producer)
    with open(f"data/{callback.from_user.id}_data.json", "r") as file:
        data = json.loads(file.read())
    if data == {}:
        await callback.answer(
            "У данного производителя нет деталей с таким артикулом в наличии, выберите другого производителя.",
            show_alert=True
        )
        return
    text = await get_params(data[choosed_producer])
    await state.update_data(choosed_producer=choosed_producer)
    await state.set_state(SGetDetail.choose_item)
    await callback.message.edit_text(
        text=text,
        reply_markup=menu.choose_item_key()
    )


@detail_router.callback_query(SGetDetail.choose_item, F.data == "back_to_prod")
async def get_producer(callback: types.CallbackQuery, state: FSMContext):
    with open(f"data/{callback.from_user.id}_data_links.json", "r") as file:
        data = json.loads(file.read())

    names = []
    for key in data.keys():
        names.append(data[key]["Названия бренда"])
    await callback.message.edit_text(
        text="Выберите производителя",
        reply_markup=menu.choose_producer_key(names=names)
    )
    await state.set_state(SGetDetail.choose_producer)


@detail_router.callback_query(SGetDetail.choose_item)
async def go_order(callback: types.CallbackQuery, state: FSMContext):

    state_data = await state.get_data()
    choosed_producer = state_data["choosed_producer"]

    with open(f"data/{callback.from_user.id}_data.json", "r") as file:
        data = json.loads(file.read())

    choose_detail = data[choosed_producer][int(callback.data)]
    await state.update_data(choose_detail=choose_detail)

    warning_text = await DatabaseAPI.get_warning_text()
    if warning_text:
        await state.set_state(SGetDetail.order)
        warning_text = warning_text
        await callback.message.edit_text(
            text=warning_text,
            reply_markup=menu.key_order()
        )
    else:
        await state.set_state(SGetDetail.point_pickup)
        points = await DatabaseAPI.get_points()
        text = "Выберите пункт самовывоза⬇️"
        await callback.message.edit_text(
            text=text,
            reply_markup=menu.key_points(points=points)
        )


@detail_router.callback_query(SGetDetail.order, F.data == "back_to_choose_detail")
async def back_to_choose_detail(callback: types.CallbackQuery, state: FSMContext):

    state_data = await state.get_data()
    choosed_producer = state_data["choosed_producer"]
    with open(f"data/{callback.from_user.id}_data.json", "r") as file:
        data = json.loads(file.read())
    text = await get_params(data[choosed_producer])

    await state.set_state(SGetDetail.choose_item)
    await callback.message.edit_text(
        text=text,
        reply_markup=menu.choose_item_key()
    )


@detail_router.callback_query(SGetDetail.order, F.data == "go_order")
async def get_point(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state(SGetDetail.point_pickup)
    points = await DatabaseAPI.get_points()
    text = "Выберите пункт самовывоза⬇️"
    await callback.message.edit_text(
        text=text,
        reply_markup=menu.key_points(points=points)
    )


@detail_router.callback_query(SGetDetail.point_pickup, F.data == "back_to_detail")
async def back_to_detail(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    choosed_producer = state_data["choosed_producer"]
    with open(f"data/{callback.from_user.id}_data.json", "r") as file:
        data = json.loads(file.read())
    text = await get_params(data[choosed_producer])

    await state.set_state(SGetDetail.choose_item)
    await callback.message.edit_text(
        text=text,
        reply_markup=menu.choose_item_key()
    )


@detail_router.callback_query(SGetDetail.point_pickup)
async def get_contacts(callback: types.CallbackQuery,
                       state: FSMContext,
                       bot: Bot):
    id_point = callback.data
    address = await DatabaseAPI.get_adress_point(id_point=id_point)
    await state.update_data(address=address)
    state_data = await state.get_data()
    choosed_producer = state_data["choosed_producer"]
    text = await get_params_one_detail(item=state_data["choose_detail"], state=state, link=choosed_producer,
                                       adress=state_data["address"])
    await state.update_data(choosed_detail=text)
    is_phone = await DatabaseAPI.check_phone(user_id=callback.from_user.id)
    if is_phone[0]:
        state_data = await state.get_data()
        await state.update_data(phone=is_phone[1]["phone_number"], name=is_phone[1]["name"])
        price = state_data["price_detail"]
        card = await DatabaseAPI.get_card()
        await state.set_state(SGetDetail.photo_pay)
        mes_ = await callback.message.edit_text(
            text=f"Отправьте {int(price)} рублей на карту <code>{card}</code> и пришлите скриншот оплаты.",
            reply_markup=menu.key_photo_pay())
        await state.update_data(mes_del=mes_.message_id)
        return
    await state.set_state(SGetDetail.contacts)
    text = "Отправьте свои контактные данные для связи. Для этого нажмите кнопку ниже⬇️"
    await callback.message.delete()
    mes = await callback.message.answer(
        text=text,
        reply_markup=menu.key_get_contacts()
    )
    await state.update_data(mes_del=mes.message_id)


@detail_router.message(SGetDetail.contacts)
async def get_photo_pay(message: types.Message,
                        state: FSMContext,
                        bot: Bot):
    contact = message.contact
    await DatabaseAPI.set_contact(phone=contact.phone_number, user_id=message.from_user.id)
    await state.update_data(phone=contact.phone_number, name=contact.first_name)
    state_data = await state.get_data()
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=state_data["mes_del"]
        )
    except:
        pass
    try:
        await message.delete()
    except:
        pass
    price = state_data["price_detail"]
    card = await DatabaseAPI.get_card()
    await state.set_state(SGetDetail.photo_pay)
    mes_ = await message.answer(f"Отправьте {int(price)} рублей на карту <code>{card}</code> и пришлите скриншот оплаты.",
                         reply_markup=menu.key_photo_pay())
    await state.update_data(mes_del=mes_.message_id)


@detail_router.message(SGetDetail.photo_pay, F.photo)
async def get_note(message: types.Message, state: FSMContext, bot: Bot):

    state_data = await state.get_data()
    photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=state_data["mes_del"]
        )
    except:
        pass
    mes = await message.answer("Напишите комментарий к заказу, либо пропустите этот шаг с помощью кнопки ниже⬇️",
                               reply_markup=menu.key_skip_note())
    await state.update_data(mes_del=mes.message_id)
    await state.set_state(SGetDetail.note)
    return


@detail_router.callback_query(SGetDetail.note, F.data == "skip_note")
async def send_photo_to_admin(callback: types.Message,
                              state: FSMContext,
                              bot: Bot):
    state_data = await state.get_data()
    group_id = await DatabaseAPI.get_channel_id()
    photo_id = state_data["photo_id"]
    caption = "<b>❗️НОВАЯ ЗАЯВКА❗️\n</b>" + state_data["choosed_detail"] + \
        f"Клиент:\n" \
        f"Телефон: {state_data['phone']}\n" \
        f"Имя: {state_data['name']}\n\n"
    result = await DatabaseAPI.add_order_to_db(user_id=callback.from_user.id,
                                               state_data=await state.get_data(), bot=bot)


    id_order = result["id"]
    caption += f"Номер заказа: #{id_order}"
    mes = await bot.send_photo(
        chat_id=group_id,
        photo=photo_id,
        caption=caption,
        reply_markup=menu.key_accept_order(user_id=callback.from_user.id, id_order=id_order)
    )
    print(mes.message_id)
    # link_message = f"https://t.me/c/{str(group_id).replace('-', '')}/{mes.message_id}"
    # print(f"Ссылка на сообщение: {mes.get_url(force_private=True)}")
    await DatabaseAPI.update_url_order(id_order=id_order, link=mes.message_id)
    # print(f"Ссылка на сообщение: {mes.get_url(force_private=True)}")
    try:
        await bot.delete_message(
            chat_id=callback.from_user.id,
            message_id=state_data["mes_del"]
        )
    except:
        pass
    await callback.message.answer("Ваша заявка на покупку отправлена и обрабатывается, ожидайте.",
                                  reply_markup=menu.go_menu())
    await state.clear()


@detail_router.message(SGetDetail.note)
async def send_photo_to_admin(message: types.Message,
                              state: FSMContext,
                              bot: Bot):
    state_data = await state.get_data()
    group_id = await DatabaseAPI.get_channel_id()
    note = message.text
    await state.update_data(note=note)
    photo_id = state_data["photo_id"]
    caption = "<b>❗️НОВАЯ ЗАЯВКА❗️\n</b>" + state_data["choosed_detail"] + \
        f"Клиент:\n" \
        f"Телефон: {state_data['phone']}\n" \
        f"Имя: {state_data['name']}\n" \
        f"Комментарий к заказу: {note}\n\n"
    result = await DatabaseAPI.add_order_to_db(user_id=message.from_user.id,
                                               state_data=await state.get_data(), bot=bot)
    id_order = result["id"]
    caption += f"Номер заказа: {id_order}"
    mes = await bot.send_photo(
        chat_id=group_id,
        photo=photo_id,
        caption=caption,
        reply_markup=menu.key_accept_order(user_id=message.from_user.id, id_order=id_order)
    )
    print(mes.message_id)
    # link_message = f"https://t.me/c/{group_id}/{mes.message_id}"
    await DatabaseAPI.update_url_order(id_order=id_order, link=mes.message_id)
    # print(f"Ссылка на сообщение: {mes.get_url(force_private=True)}")
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=state_data["mes_del"]
        )
    except:
        pass
    try:
        await message.delete()
    except:
        pass
    await message.answer("Ваша заявка на покупку отправлена и обрабатывается, ожидайте.",
                         reply_markup=menu.go_menu())
    await state.clear()


@detail_router.callback_query(F.data.contains("accept_"))
async def send_confirm(callback: types.CallbackQuery, bot: Bot):

    group_id = await DatabaseAPI.get_channel_id()
    # link_message = f"https://t.me/c/{group_id}/{callback.message.message_id}"
    order = await DatabaseAPI.get_order_by_url(url=callback.message.message_id)
    link_item = order["link_item"]
    user_id = callback.data.split("_")[-1]
    id_order = callback.data.split("_")[-2]
    await DatabaseAPI.update_approve(id_order=id_order)
    text = callback.message.caption.replace("Ссылка - Товар", f"Ссылка - <a href='{link_item}'>Товар</a>")

    # print(text)
    pattern = re.compile(r'Товар:.*?Склад', re.DOTALL)
    text_ = "<b>✅ВАША ЗАЯВКА ОДОБРЕНА✅</b>\n\n"
    result = re.search(pattern, text).group(0).replace("Склад", "").strip()
    # print(result)
    text_ += result
    await bot.send_message(
        chat_id=user_id,
        text=text_,
        reply_markup=menu.key_menu_after_success()
    )
    await callback.message.edit_caption(caption=f"{text}\n\nЗаявка одобрена✅",
                                        reply_markup=menu.key_finish_order(user_id=user_id))


@detail_router.callback_query(F.data.contains("finish_"))
async def finish_order(callback: types.CallbackQuery, bot: Bot):

    user_id = callback.data.split("_")[-1]
    group_id = await DatabaseAPI.get_channel_id()
    # link_message = f"https://t.me/c/{group_id}/{callback.message.message_id}"
    order = await DatabaseAPI.get_order_by_url(url=callback.message.message_id)
    link_item = order["link_item"]
    text = callback.message.caption.replace("Ссылка - Товар", f"Ссылка - <a href='{link_item}'>Товар</a>")
    # print(text)
    pattern = re.compile(r'Товар.*?Склад', re.DOTALL)
    text_ = "<b>ВАШ ЗАКАЗ ДОСТАВЛЕН В ПУНКТ ВЫДАЧИ</b>\n\n"
    result = re.search(pattern, text).group(0).replace("Склад", "").strip()
    # print(result)
    text_ += result
    await bot.send_message(
        chat_id=user_id,
        text=text_,
        reply_markup=menu.key_menu_after_success()
    )
    await callback.message.edit_caption(caption=f"{text}\n\nЗАКАЗ ВЫПОЛНЕН✅")


@detail_router.callback_query(F.data.contains("break_"))
async def break_order(callback: types.CallbackQuery, bot: Bot):

    group_id = await DatabaseAPI.get_channel_id()
    # link_message = f"https://t.me/c/{group_id}/{callback.message.message_id}"
    user_id = callback.data.split("_")[-1]
    order = await DatabaseAPI.get_order_by_url(url=callback.message.message_id)
    link_item = order["link_item"]
    text = callback.message.caption.replace("Ссылка - Товар", f"Ссылка - <a href='{link_item}'>Товар</a>")
    # print(text)
    pattern = re.compile(r'Товар:.*?Склад', re.DOTALL)
    text_ = "<b>ВАШ ЗАКАЗ ОТМЕНЁН ПОСТАВЩИКОМ</b>\n\n"
    result = re.search(pattern, text).group(0).replace("Склад", "").strip()
    # print(result)
    text_ += result
    await bot.send_message(
        chat_id=user_id,
        text=text_,
        reply_markup=menu.key_menu_after_success()
    )

    await callback.message.edit_caption(caption=f"{text}\n\nЗАКАЗ ОТМЕНЁН ПОСТАВЩИКОМ❌")
