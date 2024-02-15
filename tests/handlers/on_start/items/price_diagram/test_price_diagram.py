import unittest
from io import BytesIO
from unittest.mock import AsyncMock

import aiogram
import pytest
from aiogram.utils.markdown import hide_link
from aiohttp import ClientResponse
from pytest_mock import MockFixture

import keyboards
from tests.conftest import callback_query, aiogram_user

from handlers.on_start.items.price_diagram.show_price_diagram import get_diagram, upload_image_to_service, send_price_diagram
from tests import constants
from tests.constants import price_history_ex
from tests.conftest import input_message


# from handlers import upload_image_to_service


# валидный артикул и возвращается валидный спиоск цен

@pytest.mark.asyncio
@pytest.mark.parametrize("test_number", [12312312321, "12312312321"])
async def test_get_diagram_with_correct_number_and_price_list(input_message: aiogram.types.Message, mocker: MockFixture,
                                                              test_number):
    url = "URL"
    mock_get_price_history = mocker.patch("api.api_service.get_price_history", return_value=price_history_ex,
                                          new_callable=AsyncMock)
    mock_upload_image = mocker.patch(
        "handlers.on_start.items.price_diagram.show_price_diagram.upload_image_to_service",
        return_value=url, new_callable=AsyncMock)

    await get_diagram(test_number)
    mock_get_price_history.assert_awaited_once_with(int(test_number))
    mock_upload_image.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize("wrong_price_history", [None, []])
async def test_get_diagram_with_correct_number_and_empty_price_list(input_message: aiogram.types.Message,
                                                                    mocker: MockFixture, wrong_price_history):
    test_number = 12312312321
    url = "URL"
    mock_get_price_history = mocker.patch("api.api_service.get_price_history", return_value=wrong_price_history,
                                          new_callable=AsyncMock)
    mock_upload_image = mocker.patch(
        "handlers.on_start.items.price_diagram.show_price_diagram.upload_image_to_service",
        return_value=url, new_callable=AsyncMock)

    result = await get_diagram(test_number)
    assert result is None
    mock_get_price_history.assert_awaited_once_with(int(test_number))
    mock_upload_image.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_diagram_with_unexist_number(input_message: aiogram.types.Message, mocker: MockFixture):
    test_number = 12312312321
    url = "URL"
    mock_get_price_history = mocker.patch("api.api_service.get_price_history", return_value=None,
                                          new_callable=AsyncMock)
    mock_upload_image = mocker.patch(
        "handlers.on_start.items.price_diagram.show_price_diagram.upload_image_to_service",
        return_value=url, new_callable=AsyncMock)

    result = await get_diagram(test_number)
    assert result is None
    mock_get_price_history.assert_awaited_once_with(int(test_number))
    mock_upload_image.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_diagram_with_type_error_number(input_message: aiogram.types.Message, mocker: MockFixture):
    test_number = "fdfffdfdf"
    url = "URL"
    mock_get_price_history = mocker.patch("api.api_service.get_price_history", return_value=None,
                                          new_callable=AsyncMock)
    mock_upload_image = mocker.patch(
        "handlers.on_start.items.price_diagram.show_price_diagram.upload_image_to_service",
        return_value=url, new_callable=AsyncMock)

    with pytest.raises(TypeError) as ex:
        result = await get_diagram(test_number)
    mock_get_price_history.assert_not_awaited()
    mock_upload_image.assert_not_awaited()


@pytest.mark.asyncio
async def test_upload_image_to_service_positive(mocker: MockFixture):
    api_key = "test"
    img = BytesIO()

    client_response: ClientResponse = unittest.mock.create_autospec(ClientResponse, instance=True,
                                                                    new_callable=AsyncMock)
    client_response.json = AsyncMock(return_value=constants.positive_load_image_answer)
    mock_get_price_history = mocker.patch("aiohttp.ClientSession.post")
    # await upload_image_to_service(img, "Dfdfdfdf")
    mock_get_price_history.return_value.__aenter__.return_value = client_response
    image_url = await upload_image_to_service(img, api_key)
    mock_get_price_history.assert_called_once_with('https://api.imgbb.com/1/upload', params={'key': api_key},
                                                   data={'image': img})
    client_response.json.assert_awaited_once()
    assert "https" in image_url


@pytest.mark.asyncio
@pytest.mark.parametrize("response", [constants.error_load_image_answer, constants.bad_status_load_image_answer])
async def test_upload_image_to_service_fail_load(mocker: MockFixture, response):
    api_key = "test"
    img = BytesIO()

    client_response: ClientResponse = unittest.mock.create_autospec(ClientResponse, instance=True,
                                                                    new_callable=AsyncMock)
    client_response.json = AsyncMock(return_value=response)
    mock_get_price_history = mocker.patch("aiohttp.ClientSession.post")
    mock_get_price_history.return_value.__aenter__.return_value = client_response
    result = await upload_image_to_service(img, api_key)
    assert result is None
    mock_get_price_history.assert_called_once_with('https://api.imgbb.com/1/upload', params={'key': api_key},
                                                   data={'image': img})
    client_response.json.assert_awaited_once()


@pytest.mark.asyncio
async def test_upload_image_to_service_exception_occurs(mocker: MockFixture):
    api_key = "test"
    img = BytesIO()

    client_response: ClientResponse = unittest.mock.create_autospec(ClientResponse, instance=True,
                                                                    new_callable=AsyncMock)
    client_response.json = AsyncMock(return_value=constants.positive_load_image_answer,
                                     side_effect=AssertionError("Error"))
    mock_get_price_history = mocker.patch("aiohttp.ClientSession.post")
    mock_get_price_history.return_value.__aenter__.return_value = client_response
    result = await upload_image_to_service(img, api_key)
    assert result is None
    mock_get_price_history.assert_called_once_with('https://api.imgbb.com/1/upload', params={'key': api_key},
                                                   data={'image': img})
    client_response.json.assert_awaited()


@pytest.mark.asyncio
async def test_send_price_diagram_positive(mocker: MockFixture, callback_query: aiogram.types.CallbackQuery):
    callback_query_mock = AsyncMock(wraps=callback_query)
    test_url = "some_url"
    callback_query_mock.data = f'price_diagram_{constants.test_number}'
    get_diagram_mock = mocker.patch("handlers.on_start.items.price_diagram.show_price_diagram.get_diagram",
                                    return_value=test_url, new_callable=AsyncMock)
    await send_price_diagram(callback_query_mock)
    callback_query_mock.message.edit_text.assert_awaited_once_with(f'{hide_link(test_url)}График изменения цены товара',
                                                                   reply_markup=keyboards.return_to_card_item_kb(
                                                                       constants.test_number))
    get_diagram_mock.assert_awaited_once_with(str(constants.test_number))


@pytest.mark.asyncio
async def test_send_price_diagram_negative(mocker: MockFixture, callback_query: aiogram.types.CallbackQuery):
    callback_query_mock = AsyncMock(wraps=callback_query)
    test_url = None
    callback_query_mock.data = f'price_diagram_{constants.test_number}'
    get_diagram_mock = mocker.patch("handlers.on_start.items.price_diagram.show_price_diagram.get_diagram",
                                    return_value=test_url, new_callable=AsyncMock)
    await send_price_diagram(callback_query_mock)
    callback_query_mock.message.edit_text.assert_awaited_once_with(f'График изменения цены товара недоступен',
                                                                   reply_markup=keyboards.return_to_card_item_kb(
                                                                       constants.test_number))
    get_diagram_mock.assert_awaited_once_with(str(constants.test_number))


@pytest.mark.asyncio
async def test_send_price_diagram_exception(mocker: MockFixture, callback_query: aiogram.types.CallbackQuery):
    callback_query_mock = AsyncMock(wraps=callback_query)
    test_url = None
    callback_query_mock.data = f'price_diagram_{constants.test_number}'
    get_diagram_mock = mocker.patch("handlers.on_start.items.price_diagram.show_price_diagram.get_diagram",
                                    return_value=test_url, new_callable=AsyncMock, side_effect=Exception("Err"))
    with pytest.raises(Exception) as ex:
        await send_price_diagram(callback_query_mock)
    callback_query_mock.message.edit_text.assert_not_awaited()
    get_diagram_mock.assert_awaited_once_with(str(constants.test_number))
