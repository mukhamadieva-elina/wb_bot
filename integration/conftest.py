import asyncio
import logging
import sys
from unittest.mock import AsyncMock, MagicMock

from pytest_asyncio import fixture
from telethon import TelegramClient
from telethon.sessions import StringSession

import config
import main


@fixture(scope="module")
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
        async with client.conversation("@checkprice_testbot", timeout=5) as conv:
            yield conv

@fixture()
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

@fixture()
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

@fixture()
def product_item():
    product = MagicMock()
    product.Product.id = 1
    product.Product.number = 197659450
    product.Product.title = "Cолнцезащитные очки"
    product.Product.availability = True
    product.Product.price = 420.0
    return product
