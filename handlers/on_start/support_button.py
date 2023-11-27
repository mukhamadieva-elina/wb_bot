from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import keyboards
from form import Form

from handlers.router import router
from main import bot



@router.message(F.text.casefold() == '📝 написать в поддержку')
async def support(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.support)

    await message.answer(
        f'Привет! Оставьте свои пожелание разработчикам)',
        reply_markup=keyboards.return_to_menu_kb
    )



