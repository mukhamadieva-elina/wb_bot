from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from api import api_service
from api.models.item_info import get_card
from db.user_service import UserService
from form import Form

from handlers.router import router


@router.callback_query(F.data.startswith('update_tracking'))
async def update_tracking_price(callback: CallbackQuery, user_service: UserService):
    number = int(callback.data.split('update_tracking_')[1])
    await user_service.patch_start_price(callback.from_user.id, number)
    item = await user_service.get_user_product_by_number(callback.from_user.id, number)
    info, kb = get_card(api_service.get_image(int(item.Product.number)), item.Product.availability,
                        item.Product.title,
                        item.UserProduct.start_price, item.Product.price,
                        abs(item.Product.price - item.UserProduct.start_price), item.UserProduct.alert_threshold)
    try:
        await callback.message.edit_text(
            info,
            reply_markup=kb(item.Product.number)
        )
    except TelegramBadRequest:
        pass
    await callback.answer('Цена успешно изменена')
