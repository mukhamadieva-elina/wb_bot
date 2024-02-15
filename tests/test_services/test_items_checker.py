from unittest.mock import patch

import pytest

from db.product_service import ProductService
from services.items_checker import get_price_product_api, get_aval_product_api, get_changed_items


@pytest.mark.parametrize("api_obj, expected_price", [
    ([
         {"id": 197659450, "name": "Cолнцезащитные очки",
          "priceU": 199000, "salePriceU": 42000, "sizes": [
             {"name": "", "origName": "0", "rank": 0, "optionId": 320451004, "returnCost": 0,
              "stocks": []}]}], 420.0),
    ([], None)
])
def test_get_price_product_api(api_obj, expected_price):
    assert get_price_product_api(api_obj) == expected_price


@pytest.mark.parametrize("api_obj, expected_avail", [
    ([{"id": 197659450, "name": "Cолнцезащитные очки",
       "priceU": 199000, "salePriceU": 42000, "sizes": [
            {"name": "", "origName": "0", "rank": 0, "optionId": 320451004, "returnCost": 0,
             "stocks": []}]}], False),
    ([{"id": 197659450, "name": "Cолнцезащитные очки",
       "priceU": 199000, "salePriceU": 42000, "sizes": [
            {"name": "", "origName": "0", "rank": 0, "optionId": 320451004, "returnCost": 0,
             "stocks": [{'ww': 'qq'}]}]}], True),
    ([], None)
])
def test_get_aval_product_api(api_obj, expected_avail):
    assert get_aval_product_api(api_obj) == expected_avail


@pytest.mark.asyncio
async def test_get_changed_items_no_changes(product_service: ProductService, product_example):
    product_service.get_all_product.return_value = [product_example]
    with patch('api.api_service.get_product') as mock_get_product:
        mock_get_product.return_value = [
            {"id": 197659450, "name": "Cолнцезащитные очки",
             "priceU": 199000, "salePriceU": 42000, "sizes": [
                {"name": "", "origName": "0", "rank": 0, "optionId": 320451004, "returnCost": 0,
                 "stocks": [{'ww': 'aa'}]}]}]
        aval_changed_items, price_changed_items = await get_changed_items(product_service)
    assert aval_changed_items == []
    assert price_changed_items == []


@pytest.mark.asyncio
async def test_get_changed_items_aval_change(product_service: ProductService, product_example):
    product_service.get_all_product.return_value = [product_example]
    with patch('api.api_service.get_product') as mock_get_product:
        mock_get_product.return_value = [
            {"id": 197659450, "name": "Cолнцезащитные очки",
             "priceU": 199000, "salePriceU": 42000, "sizes": [
                {"name": "", "origName": "0", "rank": 0, "optionId": 320451004, "returnCost": 0,
                 "stocks": []}]}]
        aval_changed_items, price_changed_items = await get_changed_items(product_service)
    assert aval_changed_items == [(product_example.Product.number, False, -1)]
    assert price_changed_items == []

    product_example.Product.availability = False
    product_example.Product.price = -1
    with patch('api.api_service.get_product') as mock_get_product:
        mock_get_product.return_value = [
            {"id": 197659450, "name": "Cолнцезащитные очки",
             "priceU": 199000, "salePriceU": 42000, "sizes": [
                {"name": "", "origName": "0", "rank": 0, "optionId": 320451004, "returnCost": 0,
                 "stocks": [{'ww': 'qq'}]}]}]
        aval_changed_items, price_changed_items = await get_changed_items(product_service)
    assert aval_changed_items == [(product_example.Product.number, True, 420.0)]
    assert price_changed_items == []



@pytest.mark.asyncio
async def test_get_changed_items_price_change(product_service: ProductService, product_example):
    product_service.get_all_product.return_value = [product_example]
    with patch('api.api_service.get_product') as mock_get_product:
        mock_get_product.return_value = [
            {"id": 197659450, "name": "Cолнцезащитные очки",
             "priceU": 199000, "salePriceU": 52000, "sizes": [
                {"name": "", "origName": "0", "rank": 0, "optionId": 320451004, "returnCost": 0,
                 "stocks": [{'aa': 'qq'}]}]}]
        aval_changed_items, price_changed_items = await get_changed_items(product_service)
    assert aval_changed_items == []
    assert price_changed_items == [(product_example.Product.number, 520.0)]
