import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from aiogram import Dispatcher, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage

from tests.mocked_bot import MockedBot


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

