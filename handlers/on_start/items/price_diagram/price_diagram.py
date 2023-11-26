from datetime import datetime
from io import BytesIO
import requests

from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto, URLInputFile, message, input_file
from aiogram.utils.markdown import hide_link
from matplotlib import pyplot as plt

import config
import keyboards
from api import api_service

from handlers.router import router
from main import bot


@router.callback_query(F.data.startswith('price_diagram'))
async def price_diagram(callback: CallbackQuery):
    number = callback.data.split('price_diagram_')[1]
    url = await get_diagram(number)
    # message = await bot.send_document(chat_id=callback.from_user.id, document=plot, disable_notification=True)

    await callback.message.edit_text(f'{hide_link(url)}График изменения цены товара',
                                     reply_markup=keyboards.return_to_card_item_kb(number))


async def get_diagram(number):
    response = await api_service.get_price_history(int(number))
    dt = []
    price = []
    for elem in response:
        dt.append(datetime.fromtimestamp(elem['dt']))
        price.append(elem['price']['RUB'] / 100)
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(dt, price)
    img = BytesIO()
    fig.savefig(img, format='png')
    url = upload_image_to_service(img, config.api_key)
    return url


def upload_image_to_service(image_data, api_key):
    try:
        # Переход к началу данных изображения
        image_data.seek(0)

        # Загрузка изображения на сервис
        response = requests.post(
            'https://api.imgbb.com/1/upload',
            params={'key': api_key},
            files={'image': image_data}
        )

        # Парсинг JSON-ответа
        data = response.json()

        if 'error' in data:
            print('Ошибка при загрузке изображения:', data['error']['message'])
            return None

        # Проверка на успешную загрузку
        if data['status'] == 200:
            image_url = data['data']['url']
            return image_url
        else:
            print('Ошибка при загрузке изображения:', data['error']['message'])
            return None

    except Exception as e:
        print('Произошла ошибка:', str(e))
        return None
