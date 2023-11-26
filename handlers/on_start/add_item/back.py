from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from form import Form

back_from_add_item = Router()


@back_from_add_item.callback_query(F.data == 'to_menu')
async def to_menu(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Form.menu)
    await callback.message.edit_text('Вы вернулись в главное меню')
