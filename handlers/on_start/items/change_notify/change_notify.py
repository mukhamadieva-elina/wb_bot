from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import keyboards

from handlers.router import router


@router.callback_query(F.data.startswith('update_treshhold'))
async def update_treshhold(callback: CallbackQuery):
    number = int(callback.data.split('update_treshhold_')[1])
    await callback.message.edit_text('Выберите порог оповещения', reply_markup=keyboards.update_treshhold_kb(number))
