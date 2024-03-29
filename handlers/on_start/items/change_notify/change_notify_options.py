from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import keyboards
from api import api_service
from api.models import item_info
from db.user_service import UserService
from handlers.router import router


@router.callback_query(F.data.startswith('diff_'))
async def update_treshhold_to_n(callback: CallbackQuery, user_service: UserService):
    diff, percent, number = callback.data.split("_")
    user_id = callback.from_user.id
    if percent == 'always':
        await user_service.patch_alert_threshold(user_id, int(number), 0)
        user_product = await user_service.get_user_product_by_number(callback.from_user.id, int(number))
        info, kb = item_info.get_card(api_service.get_image(int(number)), user_product.Product.availability,
                                      user_product.Product.title,
                                      user_product.UserProduct.start_price,
                                      user_product.Product.price,
                                      user_product.Product.price - user_product.UserProduct.start_price,
                                      user_product.UserProduct.alert_threshold)
        await callback.message.edit_text(info,
                                         reply_markup=kb(int(number)))
    else:
        await user_service.patch_alert_threshold(user_id, int(number), int(percent))
        user_product = await user_service.get_user_product_by_number(callback.from_user.id, int(number))
        info, kb = item_info.get_card(api_service.get_image(int(number)), user_product.Product.availability,
                                      user_product.Product.title,
                                      user_product.UserProduct.start_price,
                                      user_product.Product.price,
                                      abs(user_product.Product.price - user_product.UserProduct.start_price),
                                      user_product.UserProduct.alert_threshold)
        await callback.message.edit_text(info,
                                         reply_markup=kb(number))
    await callback.answer(f'Порог успешно изменен')
