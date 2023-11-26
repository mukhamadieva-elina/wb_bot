from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto, URLInputFile, message
from aiogram.utils.markdown import hide_link

import keyboards

price_diagram_router = Router()


@price_diagram_router.callback_query(F.data == 'price_diagram')
async def price_diagram(callback: CallbackQuery):
    url = get_diagram()
    await callback.message.edit_text(f"{hide_link(url)}"
                f"вот такой график")


def get_diagram():
    return "https://yandex.ru/images/search?" \
           "from=tabbar&img_url=https%3A%2F%2Fhr-portal.ru%2Ffiles%2Fmini%2Fanaliz1." \
           "jpg&lr=2&pos=0&rpt=simage&text=график"
