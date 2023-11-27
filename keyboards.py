from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

menu_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="🛍 Мои товары"),
        KeyboardButton(text="➕ Добавить товар")
    ],
    [
        KeyboardButton(text="❓ Помощь"),
        KeyboardButton(text="📝 Написать в поддержку")
    ]
],
    resize_keyboard=True
)


# прекратить отслеживание
# изменить процент изменения стоимости товара, при котором придет оповещение (Изменить порог оповещения о колебании стоимости товара)
# отслеживать от последней измененной цены
# перейти к товару по ссылке
# посмотреть динамику цен

def item_card_available_kb(number):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Прекратить отслеживание', callback_data=f'stop_tracking_{number}')]
        ,
        [
            InlineKeyboardButton(text='Отслеживать от последней измененной цены',
                                 callback_data=f'update_tracking_{number}'),
        ],
        [
            InlineKeyboardButton(text='Изменить порог оповещения о колебании стоимости товара',
                                 callback_data=f'update_treshhold_{number}'),
        ],
        [
            InlineKeyboardButton(text='Перейти к товару по ссылке', callback_data=f'follow_the_link_{number}',
                                 url=f'https://www.wildberries.ru/catalog/{number}/detail.aspx')],

        [
            InlineKeyboardButton(text='Посмотреть динамику цен', callback_data=f'price_diagram_{number}'),
        ]
    ])


def item_card_not_available_kb(number):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Прекратить отслеживание', callback_data=f'stop_tracking_{number}')]
        ,
        [
            InlineKeyboardButton(text='Перейти к товару по ссылке', callback_data=f'follow_the_link_{number}',
                                 url=f'https://www.wildberries.ru/catalog/{number}/detail.aspx')]
    ])


return_to_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data='to_menu')]])


# при каждом изменении
# при изменении цены на 1%
# при изменении цены на 5%
# при изменении цены на 10%
# назад (при нажатии сообщение с карточкой возвращается)
def update_treshhold_kb(number):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='при каждом изменении', callback_data=f'diff_always_{number}')]
        ,
        [
            InlineKeyboardButton(text='при изменении цены на 1%', callback_data=f'diff_1_{number}'),
        ],
        [
            InlineKeyboardButton(text='при изменении цены на 5%', callback_data=f'diff_5_{number}'),
        ],
        [
            InlineKeyboardButton(text='при изменении цены на 10%', callback_data=f'diff_10_{number}')],

        [
            InlineKeyboardButton(text='Назад', callback_data=f'to_card_item_{number}'),
        ]
    ])


def return_to_card_item_kb(number):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data=f'to_card_{number}')]])
