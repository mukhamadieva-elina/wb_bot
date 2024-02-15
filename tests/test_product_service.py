import pytest
import asyncio
from wb_bot.db.product_service import ProductService


@pytest.mark.asyncio
async def test_add_product(connection, setup_db):
    product_service = ProductService(connection)
    await product_service.add_product(60594019, "1", True, 100)
    assert await product_service.product_exists_by_number(60594019)


@pytest.mark.asyncio
async def test_patch_product_with_all(connection, setup_db):
    product_service = ProductService(connection)
    await product_service.patch_product(number=60594019, aval=False, price=200)
    product = await product_service.get_product(60594019)
    assert product.Product.availability is False
    assert product.Product.price == 200


@pytest.mark.asyncio
async def test_patch_product_with_price(connection, setup_db):
    product_service = ProductService(connection)
    await product_service.patch_product(number=60594019, price=200)
    product = await product_service.get_product(60594019)
    assert product.Product.price == 200


@pytest.mark.asyncio
async def test_patch_product_with_aval(connection, setup_db):
    product_service = ProductService(connection)
    await product_service.patch_product(number=60594019, aval=False)
    product = await product_service.get_product(60594019)
    assert product.Product.availability is False


@pytest.mark.asyncio
async def test_product_exists_by_number(connection, setup_db):
    product_service = ProductService(connection)
    await product_service.add_product(60594019, "1", True, 100)
    product = await product_service.product_exists_by_number(60594019)
    assert product is True


@pytest.mark.asyncio
async def test_product_not_exists_by_number(connection, setup_db):
    product_service = ProductService(connection)
    product = await product_service.product_exists_by_number(605940191)
    assert product is False


@pytest.mark.asyncio
async def test_patch_product_price(connection, setup_db):
    product_service = ProductService(connection)
    await product_service.patch_product_price(number=60594019, price=250)
    product = await product_service.get_product(60594019)
    assert product.Product.price == 250


@pytest.mark.asyncio
async def test_patch_product_availability(connection, setup_db):
    product_service = ProductService(connection)
    await product_service.patch_product_availability(number=60594019, availability=False)
    product = await product_service.get_product(60594019)
    assert product.Product.availability is False


@pytest.mark.asyncio
async def test_get_all_product(connection, setup_db):
    product_service = ProductService(connection)
    products = await product_service.get_all_product()
    assert products


@pytest.mark.asyncio
async def test_get_user_products_by_product(connection, setup_db):
    product_service = ProductService(connection)
    user_products = await product_service.get_user_products_by_product(number=1)
    assert not user_products
