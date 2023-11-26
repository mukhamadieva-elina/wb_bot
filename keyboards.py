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

item_card_available_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Прекратить отслеживание', callback_data='stop_tracking')]
    ,
    [
        InlineKeyboardButton(text='Отслеживать от последней измененной цены', callback_data='update_tracking'),
    ],
    [
        InlineKeyboardButton(text='Изменить порог оповещения о колебании стоимости товара',
                             callback_data='update_treshhold'),
    ],
    [
        InlineKeyboardButton(text='Перейти к товару по ссылке', callback_data='follow_the_link')],

    [
        InlineKeyboardButton(text='Посмотреть динамику цен', callback_data='price_diagram'),
    ]
])
return_to_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data='to_menu')]])

# при каждом изменении
# при изменении цены на 1%
# при изменении цены на 5%
# при изменении цены на 10%
# назад (при нажатии сообщение с карточкой возвращается)
update_treshhold_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='при каждом изменении', callback_data='diff_always')]
    ,
    [
        InlineKeyboardButton(text='при изменении цены на 1%', callback_data='diff_1'),
    ],
    [
        InlineKeyboardButton(text='при изменении цены на 5%', callback_data='diff_5'),
    ],
    [
        InlineKeyboardButton(text='при изменении цены на 10%', callback_data='diff_10')],

    [
        InlineKeyboardButton(text='Назад', callback_data='to_card_item'),
    ]
])