import pytest
from sqlalchemy.exc import DBAPIError

from wb_bot.db.models import Product, UserProduct, User
from wb_bot.db.product_service import ProductService
from wb_bot.db.user_service import UserService
from sqlalchemy import insert, select

telegram_id_test = 123456
product = {'id': 5, 'number': 123, 'title': '1', 'availability': True, 'price': 100}
product2 = {'id': 7, 'number': 555, 'title': '3', 'availability': True, 'price': 1000}
user_product = {'user_telegram_id': telegram_id_test, 'start_price': 103, 'alert_threshold': 5}
user_product_for_delete = {'user_telegram_id': telegram_id_test, 'start_price': 103, 'alert_threshold': 5}


@pytest.mark.asyncio
async def test_add_user(connection):
    user_service = UserService(connection)
    await user_service.add_user(telegram_id=telegram_id_test)
    user = select(User).filter_by(telegram_id=telegram_id_test)
    assert user is not None


@pytest.mark.asyncio
async def test_add_invalid_user(connection):
    user_service = UserService(connection)
    with pytest.raises(DBAPIError):
        await user_service.add_user(telegram_id=123456789012)


@pytest.mark.asyncio
async def test_get_user(connection):
    user_service = UserService(connection)
    user = await user_service.get_user(telegram_id_test)
    assert user is not None


@pytest.mark.asyncio
async def test_get_nonexistent_user(connection):
    user_service = UserService(connection)
    user = await user_service.get_user(0)
    assert user is None


@pytest.mark.asyncio
async def test_get_user_products(connection):
    user_service = UserService(connection)

    async with connection.connect() as conn:
        await conn.execute(insert(Product).values(id=product['id'], number=product['number'], title=product['title'],
                                                  availability=product['availability'],
                                                  price=product['price']))
        await conn.execute(
            insert(UserProduct).values(user_telegram_id=user_product['user_telegram_id'], product_id=product['id'],
                                       start_price=user_product['start_price'],
                                       alert_threshold=user_product['alert_threshold']))
        await conn.commit()

    result = await user_service.get_user_products(telegram_id_test)
    assert result.__len__() == 1


@pytest.mark.asyncio
async def test_get_user_product_by_number(connection):
    user_service = UserService(connection)
    result = await user_service.get_user_product_by_number(telegram_id=telegram_id_test, number=product['number'])
    assert result[0].number == product['number']


@pytest.mark.asyncio
async def test_get_user_product_by_nonexistent_number(connection):
    user_service = UserService(connection)
    result = await user_service.get_user_product_by_number(telegram_id=telegram_id_test, number=0)
    assert result is None


@pytest.mark.asyncio
async def test_user_product_exists_by_number(connection):
    user_service = UserService(connection)
    exists = await user_service.user_product_exists_by_number(telegram_id=telegram_id_test, number=product['number'])
    assert exists


@pytest.mark.asyncio
async def test_delete_user_product(connection):
    user_service = UserService(connection)

    async with connection.connect() as conn:
        await conn.execute(insert(Product).values(id=product2['id'], number=product2['number'], title=product2['title'],
                                                  availability=product2['availability'],
                                                  price=product2['price']))
        await conn.execute(
            insert(UserProduct).values(user_telegram_id=telegram_id_test,
                                       product_id=product2['id'],
                                       start_price=user_product_for_delete['start_price'],
                                       alert_threshold=user_product_for_delete['alert_threshold']))
        await conn.commit()
    await user_service.delete_user_product(telegram_id=telegram_id_test,
                                           product_number=product2['number'])
    async with connection.connect() as conn:
        result = await conn.execute(
            select(UserProduct).filter_by(user_telegram_id=telegram_id_test,
                                          product_id=product2['id']))
    assert result.first() is None


@pytest.mark.asyncio
async def test_patch_alert_threshold(connection):
    user_service = UserService(connection)
    await user_service.patch_alert_threshold(telegram_id=telegram_id_test, product_number=product['number'],
                                             alert_threshold=5)
    async with connection.connect() as conn:
        result = await conn.execute(
            select(UserProduct).filter_by(user_telegram_id=telegram_id_test,
                                          product_id=product['id']))
    assert result.first().alert_threshold == 5


@pytest.mark.asyncio
async def test_patch_invalid_alert_threshold(connection):
    user_service = UserService(connection)
    with pytest.raises(DBAPIError):
        await user_service.patch_alert_threshold(telegram_id=telegram_id_test, product_number=product['number'],
                                                 alert_threshold='alert')


@pytest.mark.asyncio
async def test_patch_start_price(connection):
    user_service = UserService(connection)
    await user_service.patch_start_price(telegram_id=telegram_id_test, product_number=product['number']
                                         )
    async with connection.connect() as conn:
        result = await conn.execute(
            select(UserProduct).filter_by(user_telegram_id=telegram_id_test,
                                          product_id=product['id']))
    assert result.first().start_price == product['price']


@pytest.mark.asyncio
async def test_add_user_product(connection):
    user_service = UserService(connection)
    product_service = ProductService(connection)
    await user_service.add_user_product(telegram_id=telegram_id_test, number=product2['number'],
                                        product_service=product_service)
    async with connection.connect() as conn:
        result = await conn.execute(
            select(UserProduct).filter_by(user_telegram_id=telegram_id_test,
                                          product_id=product2['id']))
    assert result.first() is not None
