from datetime import datetime

import aiogram
import pytest


@pytest.fixture
def aiogram_user() -> aiogram.types.User:
    return aiogram.types.User(id=123, is_bot=False, first_name="test_user")


@pytest.fixture
def callback_query(aiogram_user: aiogram.types.User) -> aiogram.types.CallbackQuery:
    return aiogram.types.CallbackQuery(id="12312", from_user=aiogram_user, chat_instance="123132")


@pytest.fixture
def input_message(aiogram_user: aiogram.types.User) -> aiogram.types.Message:
    chat = aiogram.types.Chat(id=1, type="private")
    return aiogram.types.Message(message_id=1, date=datetime.now(), chat=chat, from_user=aiogram_user, text="testText")
