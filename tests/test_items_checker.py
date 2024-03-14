import pytest

from api import api_service
from services.items_checker import get_price_product_api, get_aval_product_api


@pytest.mark.asyncio
async def test_get_price_product_api():
    product = await api_service.get_product(106281294)
    product_data = get_price_product_api(product)
    assert product_data - 649.0 < 0.001


@pytest.mark.asyncio
async def test_aval_product_api():
    product = await api_service.get_product(106281294)
    product_data = get_aval_product_api(product)
    assert product_data is True


@pytest.mark.asyncio
async def test_not_aval_product_api():
    product = await api_service.get_product(44493335)
    product_data = get_aval_product_api(product)
    assert product_data is False
