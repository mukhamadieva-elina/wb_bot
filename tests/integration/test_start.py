import pytest
from telethon.tl.custom.message import Message
from telethon.tl.types import KeyboardButton
from telethon.tl.types import ReplyKeyboardMarkup

import utils
from tests.integration import constants
from tests.integration import conftest


@pytest.mark.asyncio(scope="module")
async def test_start(start_bot, conv):
    await conv.send_message("/start")
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
    await conv.send_message("/help")
    resp: Message = await conv.get_response()
    assert resp.text == utils.info

