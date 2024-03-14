import pytest
from pytest_mock import MockerFixture
from telethon.tl.custom.message import Message
from telethon.tl.types import ReplyInlineMarkup, KeyboardButton

from tests.integration import constants


@pytest.mark.asyncio(scope="module")
async def test_price_diagram(start_bot, conv, mocker: MockerFixture, user_product_item_1, user_product_item_2):
    link_example = 'https://basket-05.wbbasket.ru/vol815/part81575/81575967/images/big/2.webp'
    mocker.patch("db.user_service.UserService.get_user_products",
                 return_value=[user_product_item_1, user_product_item_2])
    mocker.patch('api.api_service.get_image', return_value=link_example)
    await conv.send_message("/start")
    message = await conv.get_response()
    await message.click(0, 0)
    message = await conv.get_response()
    await message.click(4)
    resp: Message = await conv.get_edit()
    reply_markup: ReplyInlineMarkup = resp.reply_markup
    all_buttons: list[KeyboardButton] = []
    for row in reply_markup.rows:
        all_buttons.extend(row.buttons)
    for button, title in zip(all_buttons, constants.expected_back_to_items_kb_text):
        assert button.text == title
    print(resp)
    assert resp.photo
