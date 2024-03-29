import asyncio

import pytest
from pytest_mock import MockerFixture
from telethon.tl.custom import Message
from telethon.tl.types import ReplyInlineMarkup

from tests.integration import constants


@pytest.mark.asyncio(scope="module")
async def test_my_items_empty(start_bot, conv, mocker: MockerFixture, user_product_item_1,
                              user_product_item_change_start_price):
    await conv.send_message("/start")
    await conv.get_response()
    link_example = constants.link_example
    mocker.patch("db.user_service.UserService.get_user_products", return_value=[user_product_item_1])
    mocker.patch('api.api_service.get_image', return_value=link_example)
    mocker.patch('db.user_service.UserService.patch_start_price')
    mocker.patch('db.user_service.UserService.get_user_product_by_number',
                 return_value=user_product_item_change_start_price)
    await conv.send_message("🛍 Мои товары")
    resp: Message = await conv.get_response()
    reply_markup: ReplyInlineMarkup = resp.reply_markup
    result = await resp.click(text='Отслеживать от последней измененной цены')
    edited_response: Message = await conv.get_edit()
    edited_reply_markup: ReplyInlineMarkup = edited_response.reply_markup
    assert edited_response.text == (f'[\u200b]({link_example})Название товара: Cолнцезащитные очки\n'
                                    f'Изначальная цена товара: 420.0'
                                    f'\nПоследняя измененная цена товара: 420.0\nРазница в цене: 0.0\n'
                                    f'Текущий порог оповещения: всегда')
    assert edited_reply_markup == reply_markup
    assert result.message == 'Цена успешно изменена'
