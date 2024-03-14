from datetime import datetime

import aiogram
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage

from tests.units.mocked_bot import MockedBot


@pytest_asyncio.fixture(scope="session")
async def storage():
    tmp_storage = MemoryStorage()
    try:
        yield tmp_storage
    finally:
        await tmp_storage.close()


@pytest.fixture(scope="session")
def bot():
    return MockedBot()


@pytest_asyncio.fixture()
async def dispatcher():
    dp = Dispatcher()
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()


@pytest.fixture(scope="session")
def state(bot, storage):
    return FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id, user_id=123, chat_id=123),
    )


@pytest.fixture()
def product_service():
    return AsyncMock()


@pytest.fixture()
def user_service():
    return AsyncMock()


@pytest.fixture()
def product_example():
    mock = MagicMock()
    mock.Product.id = 1
    mock.Product.number = 197659450
    mock.Product.title = "Cолнцезащитные очки"
    mock.Product.availability = True
    mock.Product.price = 420.0
    return mock

@pytest.fixture()
def user_product_item():
    user_product = MagicMock()
    user_product.Product.id = 1
    user_product.Product.number = 197659450
    user_product.Product.title = "Cолнцезащитные очки"
    user_product.Product.availability = True
    user_product.Product.price = 420.0
    user_product.UserProduct.user_telegram_id = 123
    user_product.UserProduct.product_id = 1
    user_product.UserProduct.start_price = 300.0
    user_product.UserProduct.alert_threshold = 0
    return [user_product]


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

