import pytest
from aiogram.client.session import aiohttp

from wb_bot.api.api_service import get_product, get_session, get_image


# TODO
@pytest.mark.asyncio
async def test_get_session():
    session = get_session('https://example.com')
    assert session is not None
    assert isinstance(session, aiohttp.ClientSession)


@pytest.mark.asyncio
async def test_get_product_valid_number():
    product_data = await get_product(106281294)
    assert product_data[0]['id'] == 106281294


@pytest.mark.asyncio
async def test_get_product_invalid_number():
    product_data = await get_product('abc')
    with pytest.raises(IndexError):
        await product_data[0]['id']


@pytest.mark.parametrize("number, expected_output", [
    (14300000, "https://basket-01.wb.ru/vol143/part14300/14300000/images/big/1.webp"),
    (14400000, "https://basket-02.wb.ru/vol144/part14400/14400000/images/big/1.webp"),
    (28700000, "https://basket-02.wb.ru/vol287/part28700/28700000/images/big/1.webp"),
    (28800000, "https://basket-03.wb.ru/vol288/part28800/28800000/images/big/1.webp"),
    (43100000, "https://basket-03.wb.ru/vol431/part43100/43100000/images/big/1.webp"),
    (43200000, "https://basket-04.wb.ru/vol432/part43200/43200000/images/big/1.webp"),
    (71900000, "https://basket-04.wb.ru/vol719/part71900/71900000/images/big/1.webp"),
    (72000000, "https://basket-05.wb.ru/vol720/part72000/72000000/images/big/1.webp"),
    (100700000, "https://basket-05.wb.ru/vol1007/part100700/100700000/images/big/1.webp"),
    (100800000, "https://basket-06.wb.ru/vol1008/part100800/100800000/images/big/1.webp"),
    (106100000, "https://basket-06.wb.ru/vol1061/part106100/106100000/images/big/1.webp"),
    (106200000, "https://basket-07.wb.ru/vol1062/part106200/106200000/images/big/1.webp"),
    (111500000, "https://basket-07.wb.ru/vol1115/part111500/111500000/images/big/1.webp"),
    (111600000, "https://basket-08.wb.ru/vol1116/part111600/111600000/images/big/1.webp"),
    (116900000, "https://basket-08.wb.ru/vol1169/part116900/116900000/images/big/1.webp"),
    (117000000, "https://basket-09.wb.ru/vol1170/part117000/117000000/images/big/1.webp"),
    (131300000, "https://basket-09.wb.ru/vol1313/part131300/131300000/images/big/1.webp"),
    (131400000, "https://basket-10.wb.ru/vol1314/part131400/131400000/images/big/1.webp"),
    (160100000, "https://basket-10.wb.ru/vol1601/part160100/160100000/images/big/1.webp"),
    (160200000, "https://basket-11.wb.ru/vol1602/part160200/160200000/images/big/1.webp"),
    (165500000, "https://basket-11.wb.ru/vol1655/part165500/165500000/images/big/1.webp"),
    (165600000, "https://basket-12.wb.ru/vol1656/part165600/165600000/images/big/1.webp"),
    (191900000, "https://basket-12.wb.ru/vol1919/part191900/191900000/images/big/1.webp"),
    (192000000, "https://basket-13.wb.ru/vol1920/part192000/192000000/images/big/1.webp"),
])
def test_get_image(number, expected_output):
    result = get_image(number)
    assert result == expected_output


@pytest.mark.parametrize("number", ['abc', '123456'])
def test_get_image_with_invalid_number(number):
    with pytest.raises(TypeError):
        get_image(number)

# TODO test_get_price_history