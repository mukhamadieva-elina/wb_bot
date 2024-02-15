import pytest
from sqlalchemy.exc import DBAPIError

from wb_bot.db.user_service import UserService

telegram_id_test = 123456


@pytest.mark.asyncio
async def test_add_user(connection):
    user_service = UserService(connection)
    await user_service.add_user(telegram_id=telegram_id_test)
    assert await user_service.get_user(telegram_id_test)


@pytest.mark.asyncio
async def test_add_invalid_user(connection):
    user_service = UserService(connection)
    with pytest.raises(DBAPIError):
        await user_service.add_user(telegram_id=123456789012)


@pytest.mark.asyncio
async def test_get_user(connection, setup_db):
    user_service = UserService(connection)
    user = await user_service.get_user(telegram_id_test)
    assert user is not None


@pytest.mark.asyncio
async def test_get_nonexistent_user(connection, setup_db):
    user_service = UserService(connection)
    user = await user_service.get_user(0)
    assert user is None


@pytest.mark.asyncio
async def test_get_user_products(connection):
    user_service = UserService(connection)
    products = await user_service.get_user_products(telegram_id_test)
    assert not products