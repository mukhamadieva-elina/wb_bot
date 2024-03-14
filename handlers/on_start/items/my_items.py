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


@router.message(F.text.casefold() == '🛍 мои товары')
async def my_items(message: Message, user_service: UserService) -> None:

    my_items = await user_service.get_user_products(message.from_user.id)

    if not my_items:
        await message.answer(
            'Вы еще ничего не добавили'
        )
    else:
        for item in my_items:
            photo = api_service.get_image(int(item.Product.number))
            info, kb = get_card(photo, item.Product.availability,
                                item.Product.title,
                                item.UserProduct.start_price, item.Product.price,
                                item.Product.price - item.UserProduct.start_price, item.UserProduct.alert_threshold)
            await message.answer(
                info,
                reply_markup=kb(item.Product.number)
            )
