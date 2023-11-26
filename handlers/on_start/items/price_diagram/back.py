from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import keyboards
from api.api_service import get_image
from api.models import item_info
from db import user_service
from db.user_service import UserService

from handlers.router import router


@router.callback_query(F.data.startswith('to_card'))
async def back_to_item_from_diagram(callback: CallbackQuery, user_service: UserService):
    number = callback.data.split('to_card_')[1]
    user_product = user_service.get_user_product_by_number(callback.from_user.id, number)
    info, kb = item_info.get_card(get_image(int(number)), user_product.Product.availability, user_product.Product.title,
                                  user_product.UserProduct.start_price,
                                  user_product.Product.price,
                                  user_product.Product.price - user_product.UserProduct.start_price,
                                  user_product.UserProduct.alert_threshold)
    await callback.message.edit_text(info, reply_markup=kb(number))
