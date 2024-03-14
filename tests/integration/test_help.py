import pytest
from telethon.tl.custom.message import Message

import utils
from tests.integration import constants


@pytest.mark.asyncio(scope="module")
async def test_help(start_bot, conv):
    await conv.send_message("/start")
    resp: Message = await conv.get_response()
    await conv.send_message(constants.help_text)
    resp: Message = await conv.get_response()
    assert resp.text == utils.info
