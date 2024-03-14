from unittest.mock import AsyncMock, patch

import pytest
from aiogram.utils.markdown import hide_link
from tests.unit.conftest import *
import keyboards
from db.user_service import UserService
from handlers import update_treshhold, back_to_item


@pytest.mark.asyncio
async def test_back_to_item(user_service: UserService, user_product_item):
    link_example = 'https://www.google.ru/'
    number = user_product_item[0].Product.number
    callback = AsyncMock(data=f'to_card_item_{number}', name='callback')
    user_service.get_user_product_by_number.return_value = user_product_item[0]
    with patch('api.api_service.get_image') as mock_get_image:
        mock_get_image.return_value = link_example
        await back_to_item(callback, user_service)
    callback.message.edit_text.assert_called_once_with(
        f"{hide_link(link_example)}Название товара: {'Cолнцезащитные очки'}\n"
        f"Изначальная цена товара: {300.0}\nПоследняя измененная цена товара: {420.0}\n"
        f"Разница в цене: {abs(120.0)}\nТекущий порог оповещения: {'всегда'}\n",
        reply_markup=keyboards.item_card_available_kb(number))
