from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import keyboards
from form import Form


from handlers.router import router


@router.message(F.text.casefold() == '➕ добавить товар')
async def add_item(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.articul)

    await message.answer(
        f'Введите артикул',
        reply_markup=keyboards.return_to_menu_kb
    )
