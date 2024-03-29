expected_start_kb_texts = ["🛍 Мои товары", "➕ Добавить товар", "❓ Помощь", "📝 Написать в поддержку"]
help_text = "❓ Помощь"
link_example = 'https://basket-05.wbbasket.ru/vol815/part81575/81575967/images/big/2.webp'
add_item_text = "➕ Добавить товар"
write_support_text = "📝 Написать в поддержку"
suport_hello_text = "Привет! Оставьте свои пожелание разработчикам)"
support_end_text = "Спасибо! Комментарий был отправлен разработчикам."
expected_back_to_items_kb_text = ["Назад"]
notifier_now_aval_values = ["Привет товар появился в наличии", f"""[​](https://basket-01.wbbasket.ru/vol0/part88/88000/images/big/1.webp)Название товара: Cолнцезащитные очки
Изначальная цена товара: 300.0
Последняя измененная цена товара: 5555
Разница в цене: 5255.0
Текущий порог оповещения: всегда"""]
notifier_now_not_aval_values = ["Привет товара больше нет в наличии", f"""[​](https://basket-01.wbbasket.ru/vol0/part88/88000/images/big/1.webp)Товара нет в наличии!
Название товара: Cолнцезащитные очки"""]

available_item_inline_keyboard_1 = [
    {'text': 'Прекратить отслеживание', 'data': b'stop_tracking_197659450'},
    {'text': 'Отслеживать от последней измененной цены', 'data': b'update_tracking_197659450'},
    {'text': 'Изменить порог оповещения о колебании стоимости товара', 'data': b'update_treshhold_197659450'},
    {'text': 'Перейти к товару по ссылке', 'url': 'https://www.wildberries.ru/catalog/197659450/detail.aspx'},
    {'text': 'Посмотреть динамику цен', 'data': b'price_diagram_197659450'}]

available_item_inline_keyboard_2 = [
    {'text': 'Прекратить отслеживание', 'data': b'stop_tracking_197659451'},
    {'text': 'Отслеживать от последней измененной цены', 'data': b'update_tracking_197659451'},
    {'text': 'Изменить порог оповещения о колебании стоимости товара', 'data': b'update_treshhold_197659451'},
    {'text': 'Перейти к товару по ссылке', 'url': 'https://www.wildberries.ru/catalog/197659451/detail.aspx'},
    {'text': 'Посмотреть динамику цен', 'data': b'price_diagram_197659451'}]