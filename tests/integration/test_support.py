import pytest
from telethon.tl.custom.message import Message
from telethon.tl.types import ReplyInlineMarkup, KeyboardButtonCallback

from tests.integration import constants


@pytest.mark.asyncio
async def test_support(connection, conv, start_bot):
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
