import pytest
from pytest_mock import MockerFixture
from telethon.tl.custom.message import Message

from tests.integration import constants


@pytest.mark.asyncio(scope="module")
async def test_stop_tracking(start_bot, conv, mocker: MockerFixture, user_product_item_1, user_product_item_2):
    link_example = constants.link_example
    mocker.patch("db.user_service.UserService.get_user_products",
                 return_value=[user_product_item_1, user_product_item_2])
    mocker.patch('api.api_service.get_image', return_value=link_example)
    mocker.patch("db.user_service.UserService.delete_user_product")
    await conv.send_message("/start")
    message = await conv.get_response()
    await message.click(0, 0)
    message = await conv.get_response()
    await message.click(0, 0)
    resp: Message = await conv.get_edit()
    assert resp.text == "Вы больше не отслеживаете этот товар"