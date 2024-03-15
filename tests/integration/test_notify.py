import pytest
from pytest_mock import MockerFixture
from sqlalchemy import delete
from telethon.helpers import TotalList

import bot
import config
from db.models import Product
from db.product_service import ProductService
from db.user_product_service import UserProductService
from db.user_service import UserService
from services import notifier
from tests.integration import constants


@pytest.mark.asyncio
async def test_notify_now_aval(mocker: MockerFixture, connection, client, user_product_item_notifier_not_aval,
                      product_item_notifier_not_aval):
    product_service = ProductService(connection)
    user_service = UserService(connection)
    item_art = product_item_notifier_not_aval.Product.number

    aval_changed_items_appear = [
        (item_art, True, 5555),
    ]

    mocker.patch("services.notifier.get_changed_items", return_value=(aval_changed_items_appear, []))
    mocker.patch("db.product_service.ProductService.get_product", return_value=product_item_notifier_not_aval)
    mocker.patch("db.product_service.ProductService.get_user_products_by_product",
                 return_value=[user_product_item_notifier_not_aval])
    link_example = 'https://basket-05.wbbasket.ru/vol815/part81575/81575967/images/big/2.webp'
    mocker.patch('api.api_service.get_image', return_value=link_example)
    mocker.patch("db.product_service.ProductService.patch_product", return_value=product_item_notifier_not_aval)

    await notifier.run(product_service, user_service, bot.bot)

    messages: list[TotalList] = await client.get_messages(config.bot_chat_name, limit=2)

    messages.reverse()
    for message, value in zip(messages, constants.notifier_now_aval_values):
        print(message.text)
        assert message.text == value


@pytest.mark.asyncio
async def test_notify_now_not_aval(mocker: MockerFixture, connection, client, user_product_item_notifier_not_aval,
                      product_item_notifier_not_aval):
    user_product_item_notifier_not_aval.Product.availability = True
    product_item_notifier_not_aval.Product.availability = True
    product_service = ProductService(connection)
    user_service = UserService(connection)
    item_art = product_item_notifier_not_aval.Product.number

    aval_changed_items_appear = [
        (item_art, False, 5555),
    ]

    mocker.patch("services.notifier.get_changed_items", return_value=(aval_changed_items_appear, []))
    mocker.patch("db.product_service.ProductService.get_product", return_value=product_item_notifier_not_aval)
    mocker.patch("db.product_service.ProductService.get_user_products_by_product",
                 return_value=[user_product_item_notifier_not_aval])
    link_example = 'https://basket-05.wbbasket.ru/vol815/part81575/81575967/images/big/2.webp'
    mocker.patch('api.api_service.get_image', return_value=link_example)
    mocker.patch("db.product_service.ProductService.patch_product", return_value=product_item_notifier_not_aval)

    await notifier.run(product_service, user_service, bot.bot)

    messages: list[TotalList] = await client.get_messages(config.bot_chat_name, limit=2)

    messages.reverse()
    for message, value in zip(messages, constants.notifier_now_not_aval_values):
        print(message.text)
        assert message.text == value