from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import keyboards

update_treshhold_router = Router()
@update_treshhold_router.callback_query(F.data == 'update_treshhold')
async def update_treshhold(callback: CallbackQuery):
    await callback.message.edit_text('Выберите порог оповещения', reply_markup=keyboards.update_treshhold_kb)
