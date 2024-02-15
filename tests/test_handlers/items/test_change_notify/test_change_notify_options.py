from unittest.mock import AsyncMock, patch

import pytest
from aiogram.utils.markdown import hide_link

import keyboards
from db.user_service import UserService
from handlers import update_treshhold_to_n


@pytest.mark.asyncio
async def test_update_treshhold_to_n_always(user_service: UserService, user_product_item):
    percent = 'always'
    number = user_product_item[0].Product.number
    link_example = 'https://www.google.ru/'
    callback = AsyncMock(data=f'diff_{percent}_{number}')
    user_service.get_user_product_by_number.return_value = user_product_item[0]
    with patch('api.api_service.get_image') as mock_get_image:
        mock_get_image.return_value = link_example
        await update_treshhold_to_n(callback, user_service)
    user_service.patch_alert_threshold.assert_called_once_with(callback.from_user.id, int(number), 0)
    callback.message.edit_text.assert_called_once_with(
        f"{hide_link(link_example)}Название товара: {'Cолнцезащитные очки'}\n"
        f"Изначальная цена товара: {300.0}\nПоследняя измененная цена товара: {420.0}\n"
        f"Разница в цене: {abs(120.0)}\nТекущий порог оповещения: {'всегда'}\n",
        reply_markup=keyboards.item_card_available_kb(number))
    callback.answer.assert_called_once_with(f'Порог успешно изменен')


@pytest.mark.asyncio
async def test_update_treshhold_to_n_5(user_service: UserService, user_product_item):
    percent = '5'
    user_product_item[0].UserProduct.alert_threshold = 5
    number = user_product_item[0].Product.number
    link_example = 'https://www.google.ru/'
    callback = AsyncMock(data=f'diff_{percent}_{number}')
    user_service.get_user_product_by_number.return_value = user_product_item[0]
    with patch('api.api_service.get_image') as mock_get_image:
        mock_get_image.return_value = link_example
        await update_treshhold_to_n(callback, user_service)
    user_service.patch_alert_threshold.assert_called_once_with(callback.from_user.id, int(number), 5)
    callback.message.edit_text.assert_called_once_with(
        f"{hide_link(link_example)}Название товара: {'Cолнцезащитные очки'}\n"
        f"Изначальная цена товара: {300.0}\nПоследняя измененная цена товара: {420.0}\n"
        f"Разница в цене: {abs(120.0)}\nТекущий порог оповещения: {'5%'}\n",
        reply_markup=keyboards.item_card_available_kb(number))
    callback.answer.assert_called_once_with(f'Порог успешно изменен')
