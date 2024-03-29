import datetime

import pytest
from pytest_mock import MockerFixture
from telethon.tl.custom.message import Message
from telethon.tl.types import ReplyInlineMarkup, KeyboardButton, MessageMediaWebPage

from tests.integration import constants


@pytest.mark.asyncio(scope="module")
async def test_price_diagram(start_bot, conv, mocker: MockerFixture, user_product_item_1):
    await conv.send_message("/start")
    await conv.get_response()
    link_example = constants.link_example
    mocker.patch("db.user_service.UserService.get_user_products",
                 return_value=[user_product_item_1])
    mocker.patch('api.api_service.get_image', return_value=link_example)
    diagram_link = "https://i.ibb.co/hFnJJz1/image.webp"
    mocker.patch("handlers.on_start.items.price_diagram.show_price_diagram.get_diagram", return_value=diagram_link)
    await conv.send_message("🛍 Мои товары")
    message: Message = await conv.get_response()
    await message.click(4)
    resp: Message = await conv.get_edit()
    reply_markup: ReplyInlineMarkup = resp.reply_markup
    all_buttons: list[KeyboardButton] = []
    for row in reply_markup.rows:
        all_buttons.extend(row.buttons)
    for button, title in zip(all_buttons, constants.expected_back_to_items_kb_text):
        assert button.text == title
    media: MessageMediaWebPage = resp.media
    assert media.webpage.url == diagram_link


