from unittest.mock import AsyncMock, create_autospec
import aiogram.types
import pytest
from aiogram import types

import db.models
import keyboards
import utils
from db.user_service import UserService
from handlers import start
from tests.conftest import input_message


@pytest.mark.asyncio
async def test_user_not_exist(input_message: aiogram.types.Message):
    mock_message: types.Message = AsyncMock(wraps=input_message)
    user_id = mock_message.from_user.id
    user_service_mock: UserService = create_autospec(UserService, instance=True)
    user_service_mock.get_user = AsyncMock(return_value=None)
    user_service_mock.add_user = AsyncMock()
    mock_message.answer = AsyncMock()

    await start.command_start(mock_message, None, user_service_mock)

    user_service_mock.get_user.assert_awaited()
    user_service_mock.add_user.assert_awaited_with(user_id)
    mock_message.answer.assert_awaited_with(utils.info, reply_markup=keyboards.menu_kb)


@pytest.mark.asyncio
async def test_user_exist(input_message):
    user = db.models.User(telegram_id=123, products=[])
    mock_message: types.Message = AsyncMock(wraps=input_message)

    user_service_mock: UserService = create_autospec(UserService, instance=True)
    user_service_mock.get_user = AsyncMock(return_value=user)
    user_service_mock.add_user = AsyncMock()
    mock_message.answer = AsyncMock()

    await start.command_start(mock_message, None, user_service_mock)

    user_service_mock.get_user.assert_awaited()
    user_service_mock.add_user.assert_not_awaited()
    mock_message.answer.assert_awaited_with(utils.info, reply_markup=keyboards.menu_kb)


@pytest.mark.asyncio
async def test_db_exception(input_message):
    user = db.models.User(telegram_id=123, products=[])
    mock_message: types.Message = AsyncMock(wraps=input_message)

    user_service_mock: UserService = create_autospec(UserService, instance=True)
    user_service_mock.get_user = AsyncMock(side_effect=Exception("boom"))

    user_service_mock.add_user = AsyncMock()
    mock_message.answer = AsyncMock()

    with pytest.raises(Exception) as ex:
        await start.command_start(mock_message, None, user_service_mock)

    mock_message.answer.assert_not_awaited()
