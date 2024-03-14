import pytest

from api.api_service import get_product, get_price_history
@pytest.mark.asyncio
def test_foo():
    assert 2 == 2

  # ТЕСТ №19
@pytest.mark.asyncio
async def test_get_product():
    product_number_test = 106281294
    product_data = await get_product(product_number_test)
    assert product_data[0]['id'] == product_number_test
    assert product_data[0]['sizes'] is not None


#   ТЕСТ №20
@pytest.mark.asyncio
async def test_get_price_history():
    product_number_test = 106281294
    result = await get_price_history(product_number_test)
    assert isinstance(result, list)
    if not result:
        return
    for item in result:
        assert 'dt' in item
        assert isinstance(item['dt'], int)
        assert 'price' in item
        assert isinstance(item['price'], dict)
        assert 'RUB' in item['price']

