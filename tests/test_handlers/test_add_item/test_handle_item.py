from unittest.mock import AsyncMock, patch, call

import pytest
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hide_link

import keyboards
from form import Form
from handlers.on_start.add_item.handle_input import process_name


@pytest.mark.asyncio
async def test_process_name_articul_incorrect(state: FSMContext, product_service, user_service):
    incorrect_articul = 'qwwe222'
    message = AsyncMock(text=incorrect_articul)
    with patch('utils.validate_articul') as mock_validate_articul:
        mock_validate_articul.return_value = False
        await process_name(message, state, product_service, user_service)
    assert await state.get_data() == {'articul': incorrect_articul}
    assert await state.get_state() == Form.articul
    message.answer.assert_called_once_with(f"Артикул некорректен, попробуйте снова!",
                                           reply_markup=keyboards.return_to_menu_kb)


@pytest.mark.asyncio
async def test_process_name_articul_correct_not_exists(state: FSMContext, product_service, user_service):
    correct_articul = '123456789'
    message = AsyncMock(text=correct_articul)
    with patch('utils.validate_articul') as mock_validate_articul:
        mock_validate_articul.return_value = True
        with patch('utils.exist_in_api') as mock_exist_in_api:
            mock_exist_in_api.return_value = None
            await process_name(message, state, product_service, user_service)
    assert await state.get_data() == {'articul': correct_articul}
    assert await state.get_state() == Form.articul
    message.answer.assert_called_once_with(f"Товара не существует попробуйте снова!",
                                           reply_markup=keyboards.return_to_menu_kb)


@pytest.mark.asyncio
async def test_process_name_articul_correct_exists_not_in_base_not_available(state: FSMContext, product_service,
                                                                             user_service):
    product_example = [
        {"id": 197659450, "name": "Cолнцезащитные очки",
         "priceU": 199000, "salePriceU": 42000, "sizes": [
            {"name": "", "origName": "0", "rank": 0, "optionId": 320451004, "returnCost": 0,
             "stocks": []}]}]
    link_example = 'https://www.google.ru/'
    correct_articul = '123456789'
    message = AsyncMock(text=correct_articul)
    product_service.get_product.return_value = False
    with patch('utils.validate_articul') as mock_validate_articul:
        mock_validate_articul.return_value = True
        with patch('utils.exist_in_api') as mock_exist_in_api:
            mock_exist_in_api.return_value = True
            with patch('api.api_service.get_product') as mock_get_product:
                mock_get_product.return_value = product_example
                with patch('api.api_service.get_image') as mock_get_image:
                    mock_get_image.return_value = link_example
                    await process_name(message, state, product_service, user_service)
    assert await state.get_data() == {'articul': correct_articul}
    assert await state.get_state() == Form.menu
    product_service.add_product.assert_called_once_with(int(correct_articul), 'Cолнцезащитные очки', False, -1)
    user_service.add_user_product.assert_called_once_with(message.from_user.id, int(correct_articul), product_service)
    message.answer.assert_has_calls([call('Товар успешно добавлен!'),
                                     call(
                                         f"{hide_link(link_example)}Товара нет в наличии!\nНазвание товара: "
                                         f"{'Cолнцезащитные очки'}\n",
                                         reply_markup=keyboards.item_card_not_available_kb(correct_articul))])


@pytest.mark.asyncio
async def test_process_name_articul_correct_exists_not_in_base_available(state: FSMContext, product_service,
                                                                         user_service):
    product_example = [
        {"id": 197659450, "name": "Cолнцезащитные очки",
         "priceU": 199000, "salePriceU": 42000, "sizes": [
            {"name": "", "origName": "0", "rank": 0, "optionId": 320451004, "returnCost": 0,
             "stocks": [{'ex': 'ample'}]}]}]
    link_example = 'https://www.google.ru/'
    correct_articul = '123456789'
    message = AsyncMock(text=correct_articul)
    product_service.get_product.return_value = False
    with patch('utils.validate_articul') as mock_validate_articul:
        mock_validate_articul.return_value = True
        with patch('utils.exist_in_api') as mock_exist_in_api:
            mock_exist_in_api.return_value = True
            with patch('api.api_service.get_product') as mock_get_product:
                mock_get_product.return_value = product_example
                with patch('api.api_service.get_image') as mock_get_image:
                    mock_get_image.return_value = link_example
                    await process_name(message, state, product_service, user_service)
    assert await state.get_data() == {'articul': correct_articul}
    assert await state.get_state() == Form.menu
    product_service.add_product.assert_called_once_with(int(correct_articul), 'Cолнцезащитные очки', True, 420.0)
    user_service.add_user_product.assert_called_once_with(message.from_user.id, int(correct_articul), product_service)
    message.answer.assert_has_calls([call('Товар успешно добавлен!'),
                                     call(
                                         f"{hide_link(link_example)}Название товара: {'Cолнцезащитные очки'}\n"
                                         f"Изначальная цена товара: {420.0}\nПоследняя измененная цена товара: {420.0}\n"
                                         f"Разница в цене: {abs(0)}\nТекущий порог оповещения: {'всегда'}\n",
                                         reply_markup=keyboards.item_card_available_kb(correct_articul))])


@pytest.mark.asyncio
async def test_process_name_articul_correct_exists_in_base_already_tracked(state: FSMContext, product_service,
                                                                           user_service, product_example):
    correct_articul = '123456789'
    message = AsyncMock(text=correct_articul)
    product_service.get_product.return_value = product_example
    user_service.user_product_exists_by_number.return_value = True
    with patch('utils.validate_articul') as mock_validate_articul:
        mock_validate_articul.return_value = True
        with patch('utils.exist_in_api') as mock_exist_in_api:
            mock_exist_in_api.return_value = True
            await process_name(message, state, product_service, user_service)
    assert await state.get_data() == {'articul': correct_articul}
    assert await state.get_state() == Form.menu
    message.answer.assert_called_once_with(f"Вы уже отслеживаете этот товар!", reply_markup=keyboards.menu_kb)


@pytest.mark.asyncio
async def test_process_name_articul_correct_exists_in_base_not_tracked(state: FSMContext, product_service,
                                                                       user_service, product_example):
    link_example = 'https://www.google.ru/'
    correct_articul = '123456789'
    message = AsyncMock(text=correct_articul)
    product_service.get_product.return_value = product_example
    user_service.user_product_exists_by_number.return_value = False
    with patch('utils.validate_articul') as mock_validate_articul:
        mock_validate_articul.return_value = True
        with patch('utils.exist_in_api') as mock_exist_in_api:
            mock_exist_in_api.return_value = True
            with patch('api.api_service.get_image') as mock_get_image:
                mock_get_image.return_value = link_example
                await process_name(message, state, product_service, user_service)
    assert await state.get_data() == {'articul': correct_articul}
    assert await state.get_state() == Form.menu
    user_service.add_user_product.assert_called_once_with(message.from_user.id, int(correct_articul), product_service)
    message.answer.assert_has_calls([call('Товар успешно добавлен!', reply_markup=keyboards.menu_kb),
                                     call(
                                         f"{hide_link(link_example)}Название товара: {'Cолнцезащитные очки'}\n"
                                         f"Изначальная цена товара: {420.0}\nПоследняя измененная цена товара: {420.0}\n"
                                         f"Разница в цене: {abs(0)}\nТекущий порог оповещения: {'всегда'}\n",
                                         reply_markup=keyboards.item_card_available_kb(correct_articul))])
