import pytest
import asyncio
from db.user_service import UserService


@pytest.mark.asyncio
async def test_add_user(connection, setup_db):
    user_service = UserService(connection)
    await user_service.add_user(telegram_id=4)
    assert await user_service.get_user(4)
