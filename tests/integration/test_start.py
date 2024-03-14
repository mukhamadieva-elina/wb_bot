import pytest
from telethon.helpers import TotalList

import bot
from services import notifier

from db.models import Product
from sqlalchemy import delete

from db.user_product_service import UserProductService

from db.product_service import ProductService

from db.user_service import UserService
from pytest_mock import MockerFixture
from telethon.tl.custom.message import Message
from telethon.tl.types import KeyboardButton, ReplyInlineMarkup, KeyboardButtonCallback
from telethon.tl.types import ReplyKeyboardMarkup

import utils
from tests.integration import constants
from tests.integration import conftest


@pytest.mark.asyncio(scope="module")
async def test_start(start_bot, conv):
    await conv.send_message("/start")
    conv.get_response()
    resp: Message = await conv.get_response()
    reply_markup: ReplyKeyboardMarkup = resp.reply_markup
    all_buttons: list[KeyboardButton] = []
    for row in reply_markup.rows:
        all_buttons.extend(row.buttons)
    for button, title in zip(all_buttons, constants.expected_start_kb_texts):
        assert button.text == title

    assert resp.text == utils.info


@pytest.mark.asyncio(scope="module")
async def test_help(start_bot, conv):
    await conv.send_message("/start")
    resp: Message = await conv.get_response()
    await conv.send_message(constants.help_text)
    resp: Message = await conv.get_response()
    assert resp.text == utils.info


@pytest.mark.asyncio(scope="module")
async def test_mock(start_bot, conv, mocker: MockerFixture):
    # get_card_mock = mocker.patch("db.user_service.UserService.get_user", return_value=None)

    await conv.send_message("/start")
    resp: Message = await conv.get_response()
    print(resp)


@pytest.mark.asyncio
async def test_notify(mocker: MockerFixture, connection, client):
    product_service = ProductService(connection)
    user_service = UserService(connection)
    item_art = 88000
    user_product_service = UserProductService(connection)
    test_user_1 = {"telegram_id": 480316781}
    test_product_1 = {"number": item_art, "title": "test_prod_1", "aval": False, "price": 5000}

    await user_service.delete_user_product(telegram_id=test_user_1["telegram_id"],
                                           product_number=test_product_1["number"])
    async with connection.connect() as conn:
        await conn.execute(delete(Product).where(Product.number == test_product_1["number"]))
        await conn.commit()

    await product_service.add_product(number=test_product_1["number"], title=test_product_1["title"],
                                      availability=test_product_1["aval"], price=test_product_1["price"])
    # await user_service.add_user()
    await user_service.add_user_product(telegram_id=test_user_1["telegram_id"], number=test_product_1["number"],
                                        product_service=product_service)

    aval_changed_items_appear = [
        (item_art, True, 5555),
    ]
    aval_changed_items_disappear = [
        (item_art, False, 5555),
    ]
    mocker_data = mocker.patch("services.notifier.get_changed_items")
    mocker_data.side_effect = [(aval_changed_items_appear, []), (aval_changed_items_disappear, [])]

    await notifier.run(product_service, user_service, bot.bot)
    await notifier.run(product_service, user_service, bot.bot)

    messages: list[TotalList] = await client.get_messages('@xenob8bot', limit=4)

    messages.reverse()
    for message, value in zip(messages, constants.notifier_expected_values):
        assert message.text == value

    await user_service.delete_user_product(telegram_id=test_user_1["telegram_id"],
                                           product_number=test_product_1["number"])
    async with connection.connect() as conn:
        await conn.execute(delete(Product).where(Product.number == test_product_1["number"]))
        await conn.commit()


@pytest.mark.asyncio
async def test_notify(connection, conv, start_bot):
    await conv.send_message("/start")
    await conv.get_response()
    await conv.send_message(constants.write_support_text)
    resp: Message = await conv.get_response()
    assert resp.text == constants.suport_hello_text
    reply_markup: ReplyInlineMarkup = resp.reply_markup
    all_buttons: list[KeyboardButtonCallback] = []
    for row in reply_markup.rows:
        all_buttons.extend(row.buttons)
    cb_button = all_buttons[0]
    assert cb_button.text == 'Назад'
    assert cb_button.data == b'to_menu'
    test_support_msg = "there are huge problems in bot"
    await conv.send_message(test_support_msg)
    resp = await conv.get_response()
    assert resp.text == test_support_msg
    resp = await conv.get_response()
    assert resp.text == constants.support_end_text

