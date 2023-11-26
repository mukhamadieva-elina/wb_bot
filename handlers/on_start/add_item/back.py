from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import keyboards
from form import Form

from handlers.router import router


@router.callback_query(F.data == 'to_menu')
async def to_menu(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Form.menu)
    await callback.message.edit_text('Вы вернулись в главное меню')
