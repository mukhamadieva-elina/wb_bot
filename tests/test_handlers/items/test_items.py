from unittest.mock import AsyncMock, patch, call

import pytest
from aiogram.utils.markdown import hide_link

import keyboards
from db.user_service import UserService
from handlers.on_start.items import my_items


@pytest.mark.asyncio
async def test_items_not_exist(user_service: UserService):
    message = AsyncMock(text='🛍 мои товары')
    user_service.get_user_products.return_value = None
    await my_items(message, user_service)
    message.answer.assert_called_once_with(
        'Вы еще ничего не добавили'
    )


@pytest.mark.asyncio
async def test_items_exist_one_item(user_service: UserService, user_product_item):
    message = AsyncMock(text='🛍 мои товары')
    link_example = 'https://www.google.ru/'
    user_service.get_user_products.return_value = user_product_item
    with patch('api.api_service.get_image') as mock_get_image:
        mock_get_image.return_value = link_example
        await my_items(message, user_service)
    message.answer.assert_called_once_with(
        f"{hide_link(link_example)}Название товара: {'Cолнцезащитные очки'}\n"
        f"Изначальная цена товара: {300.0}\nПоследняя измененная цена товара: {420.0}\n"
        f"Разница в цене: {abs(120.0)}\nТекущий порог оповещения: {'всегда'}\n",
        reply_markup=keyboards.item_card_available_kb(197659450))


@pytest.mark.asyncio
async def test_items_exist_several_items(user_service: UserService, user_product_item):
    message = AsyncMock(text='🛍 мои товары')
    link_example = 'https://www.google.ru/'
    user_service.get_user_products.return_value = user_product_item * 3
    with patch('api.api_service.get_image') as mock_get_image:
        mock_get_image.return_value = link_example
        await my_items(message, user_service)
    call_my_items = call(f"{hide_link(link_example)}Название товара: {'Cолнцезащитные очки'}\n"
                         f"Изначальная цена товара: {300.0}\nПоследняя измененная цена товара: {420.0}\n"
                         f"Разница в цене: {abs(120.0)}\nТекущий порог оповещения: {'всегда'}\n",
                         reply_markup=keyboards.item_card_available_kb(197659450))
    message.answer.assert_has_calls([call_my_items] * 3)
