from wb_bot.api.models.item_info import get_card


def test_get_card_available():
    link = "example.com"
    availability = True
    title = "Test Product"
    start_price = 100
    last_price = 90
    diff_price = -10
    treshhold = 5

    result, _ = get_card(link, availability, title, start_price, last_price, diff_price, treshhold)

    assert "Название товара: Test Product" in result
    assert "Изначальная цена товара: 100" in result
    assert "Последняя измененная цена товара: 90" in result
    assert "Разница в цене: 10" in result
    assert "Текущий порог оповещения: 5%" in result


def test_get_card_not_available():
    link = "example.com"
    availability = False
    title = "Test Product"
    start_price = 100
    last_price = 90
    diff_price = -10
    treshhold = 5

    result, _ = get_card(link, availability, title, start_price, last_price, diff_price, treshhold)

    assert "Товара нет в наличии!" in result
    assert "Название товара: Test Product" in result


def test_get_not_treshhold():
    link = "example.com"
    availability = True
    title = "Test Product"
    start_price = 100
    last_price = 90
    diff_price = -10
    treshhold = 0

    result, _ = get_card(link, availability, title, start_price, last_price, diff_price, treshhold)

    assert "Название товара: Test Product" in result
    assert "Изначальная цена товара: 100" in result
    assert "Последняя измененная цена товара: 90" in result
    assert "Разница в цене: 10" in result
    assert "Текущий порог оповещения: всегда" in result
