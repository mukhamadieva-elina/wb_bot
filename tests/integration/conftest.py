import asyncio
import logging
import sys
from unittest.mock import MagicMock

import pytest
from pytest_asyncio import fixture
from sqlalchemy.ext.asyncio import create_async_engine
from telethon import TelegramClient
from telethon.sessions import StringSession

import config
import main

test_bd_pass = config.test_bd_pass

@pytest.fixture(scope="session")
def event_loop():
    """
    Creates an instance of the default event loop for the test session.
    """
    if sys.platform.startswith("win") and sys.version_info[:2] >= (3, 8):
        # Avoid "RuntimeError: Event loop is closed" on Windows when tearing down tests
        # https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# @pytest.fixture(scope="session")
# def event_loop():
#     loop = asyncio.get_event_loop()
#     yield loop
#     loop.close()
# @pytest.fixture(scope="session")
# def event_loop():
#     return asyncio.get_event_loop()


@fixture(scope="session")
async def start_bot():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    print("running bot")
    task = asyncio.create_task(main.main())
    await asyncio.sleep(5)
    yield


@fixture(scope="module")
async def conv():
    api_id = config.api_id
    api_hash = config.api_hash
    session_str = config.session_str

    client = TelegramClient(StringSession(session_str), api_id, api_hash, system_version="4.16.30-vxCUSTOM")

    async with client:

        async with client.conversation(config.bot_chat_name, timeout=5) as conv:
            yield conv

@fixture(scope="module")
async def client():
    api_id = config.api_id
    api_hash = config.api_hash
    session_str = config.session_str

    client = TelegramClient(StringSession(session_str), api_id, api_hash, system_version="4.16.30-vxCUSTOM")

    async with client:
        yield client


# @pytest.fixture(scope='session')
# def event_loop():
#     """
#     Creates an instance of the default event loop for the test session.
#     """
#     policy = asyncio.get_event_loop_policy()
#     loop = policy.new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(scope="session")
def connection():
    engine = create_async_engine(
        f"postgresql+asyncpg://dyvawvhc:{test_bd_pass}@trumpet.db.elephantsql.com/dyvawvhc"
    )
    return engine

@pytest.fixture()
def user_product_item_1():
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
    return user_product

@pytest.fixture()
def user_product_item_2():
    user_product = MagicMock()
    user_product.Product.id = 2
    user_product.Product.number = 197659451
    user_product.Product.title = "Cолнцезащитные очки"
    user_product.Product.availability = True
    user_product.Product.price = 420.0
    user_product.UserProduct.user_telegram_id = 123
    user_product.UserProduct.product_id = 2
    user_product.UserProduct.start_price = 300.0
    user_product.UserProduct.alert_threshold = 10
    return user_product

@pytest.fixture()
def product_item():
    product = MagicMock()
    product.Product.id = 1
    product.Product.number = 197659450
    product.Product.title = "Cолнцезащитные очки"
    product.Product.availability = True
    product.Product.price = 420.0
    return product

@pytest.fixture()
def user_product_item_notifier_not_aval():
    user_product = MagicMock()
    user_product.Product.id = 1
    user_product.Product.number = 88000
    user_product.Product.title = "Cолнцезащитные очки"
    user_product.Product.availability = False
    user_product.Product.price = 420.0
    user_product.UserProduct.user_telegram_id = config.admin_id
    user_product.UserProduct.product_id = 1
    user_product.UserProduct.start_price = 300.0
    user_product.UserProduct.alert_threshold = 0
    return user_product

@pytest.fixture()
def product_item_notifier_not_aval():
    product = MagicMock()
    product.Product.id = 1
    product.Product.number = 88000
    product.Product.title = "Cолнцезащитные очки"
    product.Product.availability = False
    product.Product.price = 420.0
    return product

@fixture()
def user_product_item_change_start_price(user_product_item_1):
    user_product = MagicMock()
    user_product.Product.id = 1
    user_product.Product.number = 197659450
    user_product.Product.title = "Cолнцезащитные очки"
    user_product.Product.availability = True
    user_product.Product.price = 420.0
    user_product.UserProduct.user_telegram_id = 123
    user_product.UserProduct.product_id = 1
    user_product.UserProduct.start_price = 420.0
    user_product.UserProduct.alert_threshold = 0
    return user_product
