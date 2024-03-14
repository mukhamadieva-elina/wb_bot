import pytest
from pytest_mock import MockerFixture
from telethon.tl.custom.message import Message
from telethon.tl.types import KeyboardButton
from telethon.tl.types import ReplyInlineMarkup

from tests.integration import constants


@pytest.mark.asyncio(scope="module")
async def test_my_items_empty(start_bot, conv, mocker: MockerFixture):
    await conv.send_message("/start")
    await conv.get_response()
    mocker.patch("db.user_service.UserService.get_user_products", return_value=None)
    await conv.send_message("🛍 Мои товары")
    resp: Message = await conv.get_response()
    print(resp)
    assert resp.text == 'Вы еще ничего не добавили'


@pytest.mark.asyncio(scope="module")
async def test_my_items_not_empty(start_bot, conv, mocker: MockerFixture, user_product_item_1, user_product_item_2):
    await conv.send_message("/start")
    await conv.get_response()
    link_example = 'https://basket-05.wbbasket.ru/vol815/part81575/81575967/images/big/2.webp'
    mocker.patch("db.user_service.UserService.get_user_products",
                 return_value=[user_product_item_1, user_product_item_2])
    mocker.patch('api.api_service.get_image', return_value=link_example)

    await conv.send_message("🛍 Мои товары")
    resp_1: Message = await conv.get_response()
    resp_2: Message = await conv.get_response()

    reply_markup_1: ReplyInlineMarkup = resp_1.reply_markup
    reply_markup_2: ReplyInlineMarkup = resp_2.reply_markup

    all_buttons_1: list[KeyboardButton] = []
    all_buttons_2: list[KeyboardButton] = []

    assert (resp_1.text == f"[\u200b]({link_example})Название товара: {'Cолнцезащитные очки'}\n"
                           f"Изначальная цена товара: {300.0}\nПоследняя измененная цена товара: {420.0}\n"
                           f"Разница в цене: {abs(120.0)}\nТекущий порог оповещения: {'всегда'}")
    assert (resp_2.text == f"[\u200b]({link_example})Название товара: {'Cолнцезащитные очки'}\n"
                           f"Изначальная цена товара: {300.0}\nПоследняя измененная цена товара: {420.0}\n"
                           f"Разница в цене: {abs(120.0)}\nТекущий порог оповещения: 10%")

    for row in reply_markup_1.rows:
        all_buttons_1.extend(row.buttons)
    for button, resp_kb in zip(all_buttons_1, constants.available_item_inline_keyboard_1):
        assert button.text == resp_kb['text']
        if 'data' in resp_kb:
            assert button.data == resp_kb['data']
        if 'url' in resp_kb:
            assert button.url == resp_kb['url']

    for row in reply_markup_2.rows:
        all_buttons_2.extend(row.buttons)
    for button, resp_kb in zip(all_buttons_2, constants.available_item_inline_keyboard_2):
        assert button.text == resp_kb['text']
        if 'data' in resp_kb:
            assert button.data == resp_kb['data']
        if 'url' in resp_kb:
            assert button.url == resp_kb['url']
