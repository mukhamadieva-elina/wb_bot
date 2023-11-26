from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import keyboards
from form import Form

from handlers.router import router
from main import bot


@router.message(Form.menu, F.text.casefold() == '📝 написать в поддержку')
async def add_item(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.support)

    await message.answer(
        f'Привет! Оставьте свои пожелание разработчикам)',
        reply_markup=keyboards.return_to_menu_kb
    )


@router.message(Form.support)
async def process_msg_to_support(message: Message, state: FSMContext) -> None:
    await state.update_data(support=message.text)
    await state.set_state(Form.menu)
    await bot.send_message(491198715, message.text)
    await message.answer('Спасибо! Комментарий был отправлен разработчикам.', reply_markup=keyboards.menu_kb)
