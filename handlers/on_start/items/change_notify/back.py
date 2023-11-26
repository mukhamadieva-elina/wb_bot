from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import keyboards

back_from_update_treshhold_router = Router()


@back_from_update_treshhold_router.callback_query(F.data.startswith('to_card_item'))
async def back_to_item(callback: CallbackQuery):
    await callback.message.edit_text(f'тут кароче карточку наверн отрисовываем',
                                     reply_markup=keyboards.item_card_available_kb)
