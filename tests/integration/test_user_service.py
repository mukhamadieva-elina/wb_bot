import pytest

from db.models import UserProduct, Product, User
from db.product_service import ProductService
from db.user_service import UserService
from sqlalchemy import insert, select, delete, update


#   ТЕСТ №2
@pytest.mark.asyncio
async def test_patch_start_price(connection):
    telegram_id_test = 12345
    product = {'id': 1000, 'number': 1230, 'title': '1', 'availability': True, 'price': 100}
    user_service = UserService(connection)
    session = user_service.session

    async with connection.connect() as conn:
        await conn.execute(insert(User).values(telegram_id=telegram_id_test))
        await conn.execute(insert(Product).values(id=product['id'], number=product['number'], title=product['title'],
                                                  availability=product['availability'], price=product['price']))
        await conn.execute(insert(UserProduct).values(user_telegram_id=telegram_id_test, product_id=product['id'],
                                                      start_price=product['price'], alert_threshold=0))

        new_price = product['price'] + 1
        await conn.execute(update(Product).where(Product.id == product['id']).values(price=new_price))
        await conn.commit()

        await user_service.patch_start_price(telegram_id=telegram_id_test, product_number=product['number'],
                                             session=conn)
        result = await conn.execute(
            select(UserProduct).filter_by(user_telegram_id=telegram_id_test,
                                          product_id=product['id']))

        await conn.execute(delete(UserProduct).where(UserProduct.user_telegram_id == telegram_id_test).where(
            UserProduct.product_id == product['id']))
        await conn.execute(delete(User).where(User.telegram_id == telegram_id_test))
        await conn.execute(delete(Product).where(Product.id == product['id']))
        await conn.commit()
        assert result.first().start_price == new_price


#   ТЕСТ №18
@pytest.mark.asyncio
async def test_add_user(connection):
    telegram_id_test = 12345
    user_service = UserService(connection)
    session = user_service.session
    async with connection.connect() as conn:
        await user_service.add_user(telegram_id=telegram_id_test, session=conn)
        query = select(User).filter_by(telegram_id=telegram_id_test)
        result = await conn.execute(query)
        user = result.first()
        if user:
            await conn.execute(delete(User).where(User.telegram_id == telegram_id_test))
            await conn.commit()
        assert user is not None


@pytest.mark.asyncio
async def test_add_user_product(connection):
    product = {'id': 1000, 'number': 1230, 'title': '1', 'availability': True, 'price': 100}
    user_service = UserService(connection)
    session = user_service.session
    telegram_id_test = 12345
    product_service = ProductService(connection)
    async with connection.connect() as conn:
        await conn.execute(insert(Product).values(id=product['id'], number=product['number'], title=product['title'],
                                                  availability=product['availability'], price=product['price']))
        await conn.execute(insert(User).values(telegram_id=telegram_id_test))
        await conn.commit()
        await user_service.add_user_product(telegram_id=telegram_id_test, number=product['number'],
                                            product_service=product_service, session=conn)

        result = await conn.execute(
            select(UserProduct).filter_by(user_telegram_id=telegram_id_test,
                                          product_id=product['id']))
        if result:
            await conn.execute(delete(UserProduct).where(UserProduct.user_telegram_id == telegram_id_test).where(
                UserProduct.product_id == product['id']))
            await conn.execute(delete(User).where(User.telegram_id == telegram_id_test))
            await conn.execute(delete(Product).where(Product.id == product['id']))
            await conn.commit()
        assert result.first() is not None


@pytest.mark.asyncio
async def test_delete_user_product(connection):
    product = {'id': 1000, 'number': 1230, 'title': '1', 'availability': True, 'price': 100}
    user_service = UserService(connection)
    telegram_id_test = 12345
    async with connection.connect() as conn:
        await conn.execute(insert(Product).values(id=product['id'], number=product['number'], title=product['title'],
                                                  availability=product['availability'], price=product['price']))
        await conn.execute(insert(User).values(telegram_id=telegram_id_test))
        await conn.execute(insert(UserProduct).values(user_telegram_id=telegram_id_test, product_id=product['id'],
                                                      start_price=product['price'], alert_threshold=0))
        await conn.commit()
        await user_service.delete_user_product(telegram_id=telegram_id_test,
                                               product_number=product['number'], session=conn)
        result = await conn.execute(
                select(UserProduct).filter_by(user_telegram_id=telegram_id_test,
                                              product_id=product['id']))
        if result:
            await conn.execute(delete(UserProduct).where(UserProduct.user_telegram_id == telegram_id_test).where(
                UserProduct.product_id == product['id']))
            await conn.execute(delete(User).where(User.telegram_id == telegram_id_test))
            await conn.execute(delete(Product).where(Product.id == product['id']))
            await conn.commit()
    assert result.first() is None

