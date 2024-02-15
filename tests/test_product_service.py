import pytest
import asyncio
from db.product_service import ProductService


@pytest.mark.asyncio
async def test_add_product(connection, setup_db):
    user_service = ProductService(connection)
    await user_service.add_product(60594019, "1", True, 100)
    assert await user_service.product_exists_by_number(60594019)


