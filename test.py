from datetime import datetime
from unittest.mock import AsyncMock, create_autospec, patch

import pytest
from aiogram import types
from echo_handler import command_start_handler


@pytest.mark.asyncio
async def test_command_start_positive():
    # Создаем мок объекта Message с минимально необходимыми полями для создания возвращаемого значения
    chat = types.Chat(id=123456789, type="private")
    return_value_message = types.Message(message_id=1, date=datetime.now(), chat=chat)

    message_mock = create_autospec(types.Message, instance=True)
    # Настраиваем мок метода reply для возвращения предварительно созданного объекта Message
    message_mock.reply = AsyncMock(return_value=return_value_message)

    # Вызываем обработчик команды
    await command_start_handler(message_mock)

    # Проверяем, был ли вызван метод reply с ожидаемым сообщением
    message_mock.reply.assert_awaited_with("Привет! Я твой бот.")

@pytest.mark.asyncio
@patch.object(types.Message, "reply", new_callable=AsyncMock)
async def test_command_start_positive_1(msg_mock):
    # Создаем мок объекта Message с минимально необходимыми полями для создания возвращаемого значения
    chat = types.Chat(id=123456789, type="private")
    return_value_message = types.Message(message_id=1, date=datetime.now(), chat=chat)
    msg = types.Message(message_id=1, date=datetime.now(), chat=chat, text="hi")

    msg_mock.return_value = return_value_message

    # Вызываем обработчик команды
    await command_start_handler(msg)

    # Проверяем, был ли вызван метод reply с ожидаемым сообщением
    msg_mock.assert_awaited_with("Привет! Я твой бот.")



@pytest.mark.asyncio
async def test_command_start_positive__():
    # Создаем мок объекта Message с минимально необходимыми полями для создания возвращаемого значения
    chat = types.Chat(id=123456789, type="private")
    return_value_message = types.Message(message_id=1, date=datetime.now(), chat=chat)
    with patch.object(types.Message, "reply", new_callable=AsyncMock) as mock_reply:
        # mock_reply.return_value = return_value_message
        await command_start_handler(return_value_message)
        mock_reply.assert_awaited_with("Привет! Я твой бот.")
