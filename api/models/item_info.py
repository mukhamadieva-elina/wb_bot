from aiogram.utils.markdown import hide_link

import keyboards


def get_card(link, availability, title, start_price, last_price, diff_price, treshhold):
    if availability:
        if not treshhold:
            convert_treshhold = 'всегда'
        else:
            convert_treshhold = str(treshhold) + '%'
        return f"{hide_link(link)}Название товара: {title}\n" \
               f"Изначальная цена товара: {start_price}\nПоследняя измененная цена товара: {last_price}\n" \
               f"Разница в цене: {abs(diff_price)}\nТекущий порог оповещения: {convert_treshhold}\n", \
            keyboards.item_card_available_kb
    else:
        return f"{hide_link(link)}Товара нет в наличии!\nНазвание товара: {title}\n", \
            keyboards.item_card_not_available_kb
