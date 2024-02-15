import pytest

from services.items_checker import get_price_product_api, get_aval_product_api


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