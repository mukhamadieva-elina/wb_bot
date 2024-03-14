import pytest
from pytest_mock import MockerFixture
from sqlalchemy import delete
from telethon.helpers import TotalList

import bot
from db.models import Product
from db.product_service import ProductService
from db.user_product_service import UserProductService
from db.user_service import UserService
from services import notifier
from tests.integration import constants


@pytest.mark.asyncio
async def test_notify(mocker: MockerFixture, connection, client):
    product_service = ProductService(connection)
    user_service = UserService(connection)
    item_art = 88000
    user_product_service = UserProductService(connection)
    test_user_1 = {"telegram_id": 480316781}
    test_product_1 = {"number": item_art, "title": "test_prod_1", "aval": False, "price": 5000}

    await user_service.delete_user_product(telegram_id=test_user_1["telegram_id"],
                                           product_number=test_product_1["number"])
    async with connection.connect() as conn:
        await conn.execute(delete(Product).where(Product.number == test_product_1["number"]))
        await conn.commit()

    await product_service.add_product(number=test_product_1["number"], title=test_product_1["title"],
                                      availability=test_product_1["aval"], price=test_product_1["price"])
    # await user_service.add_user()
    await user_service.add_user_product(telegram_id=test_user_1["telegram_id"], number=test_product_1["number"],
                                        product_service=product_service)

    aval_changed_items_appear = [
        (item_art, True, 5555),
    ]
    aval_changed_items_disappear = [
        (item_art, False, 5555),
    ]
    mocker_data = mocker.patch("services.notifier.get_changed_items")
    mocker_data.side_effect = [(aval_changed_items_appear, []), (aval_changed_items_disappear, [])]

    await notifier.run(product_service, user_service, bot.bot)
    await notifier.run(product_service, user_service, bot.bot)

    messages: list[TotalList] = await client.get_messages('@xenob8bot', limit=4)

    messages.reverse()
    for message, value in zip(messages, constants.notifier_expected_values):
        assert message.text == value

    await user_service.delete_user_product(telegram_id=test_user_1["telegram_id"],
                                           product_number=test_product_1["number"])
    async with connection.connect() as conn:
        await conn.execute(delete(Product).where(Product.number == test_product_1["number"]))
        await conn.commit()
