import pytest
from pytest_mock import MockerFixture
from telethon.tl.custom import Message
from telethon.tl.types import ReplyInlineMarkup


@pytest.mark.asyncio(scope="module")
async def test_my_items_empty(start_bot, conv, mocker: MockerFixture, user_product_item_1):
    await conv.send_message("/start")
    await conv.get_response()
    mocker.patch("db.user_service.UserService.get_user_products", return_value=[user_product_item_1])
    await conv.send_message("🛍 Мои товары")
    resp: Message = await conv.get_response()
    reply_markup: ReplyInlineMarkup = resp.reply_markup
    for button_row in reply_markup.rows:
        if button_row.buttons[0].text == 'Отслеживать от последней измененной цены':
            pass

    print(resp)
