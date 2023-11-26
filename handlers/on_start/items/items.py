from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputFile
from aiogram.utils.markdown import hide_link

import keyboards
from api import api_service
from db.product_service import ProductService
from db.user_service import UserService
from form import Form
from api.models.item_info import get_card

from handlers.router import router


def get_items(user_id, user_service: UserService):
    # Запрос к базе
    return user_service.get_user_products(user_id)


@router.message(Form.menu, F.text.casefold() == '🛍 мои товары')
async def my_items(message: Message, user_service: UserService) -> None:
    my_items = get_items(message.from_user.id, user_service)
    if not my_items:
        await message.answer(
            'Вы еще ничего не добавили'
        )
    else:
        for item in my_items:
            info, kb = get_card(api_service.get_image(int(item.Product.number)), item.Product.availability,
                                item.Product.title,
                                item.UserProduct.start_price, item.Product.price,
                                item.Product.price - item.UserProduct.start_price, item.UserProduct.alert_threshold)
            await message.answer(
                info,
                reply_markup=kb(item.Product.number)
            )
