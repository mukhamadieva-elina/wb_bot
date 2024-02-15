from datetime import datetime
from io import BytesIO

import aiohttp

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hide_link
from matplotlib import pyplot as plt

import config
import keyboards
from api import api_service

from handlers.router import router


@router.callback_query(F.data.startswith('price_diagram'))
async def price_diagram(callback: CallbackQuery):
    number = callback.data.split('price_diagram_')[1]
    url = await get_diagram(number)
    # message = await bot.send_document(chat_id=callback.from_user.id, document=plot, disable_notification=True)
    if url:
        await callback.message.edit_text(f'{hide_link(url)}График изменения цены товара',
                                         reply_markup=keyboards.return_to_card_item_kb(number))
    else:
        await callback.message.edit_text(f'График изменения цены товара недоступен',
                                         reply_markup=keyboards.return_to_card_item_kb(number))


async def get_diagram(number):
    response = await api_service.get_price_history(int(number))
    dt = []
    price = []
    for elem in response:
        dt.append(datetime.fromtimestamp(elem['dt']))
        price.append(elem['price']['RUB'] / 100)
    if not len(dt):
        return None
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(dt, price)
    img = BytesIO()
    fig.savefig(img, format='webp')
    url = await upload_image_to_service(img, config.api_key)
    return url


async def upload_image_to_service(image_data, api_key):
    try:
        # Переход к началу данных изображения
        image_data.seek(0)

        async with aiohttp.ClientSession() as session:
            # Загрузка изображения на сервис
            async with session.post(
                    'https://api.imgbb.com/1/upload',
                    params={'key': api_key},
                    data={'image': image_data}
            ) as response:
                # Парсинг JSON-ответа
                data = await response.json()

                if 'error' in data:
                    print('Ошибка при загрузке изображения:', data['error']['message'])
                    return None

                # Проверка на успешную загрузку
                if data['status'] == 200:
                    image_url = data['data']['image']['url']
                    return image_url
                else:
                    print('Ошибка при загрузке изображения:', data['error']['message'])
                    return None

    except Exception as e:
        print('Произошла ошибка:', str(e))
        return None
