from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import keyboards
from form import Form

from handlers.router import router
from main import bot


@router.message(Form.support)
async def process_msg_to_support(message: Message, state: FSMContext) -> None:
    # await state.update_data(support=message.text)
    await bot.send_message(491198715, message.text)
    await message.answer('Спасибо! Комментарий был отправлен разработчикам.', reply_markup=keyboards.menu_kb)
    await state.clear()





