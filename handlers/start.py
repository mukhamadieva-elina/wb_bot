from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import keyboards
import utils
from db.user_service import UserService
from handlers.router import router


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext, user_service: UserService) -> None:
    # После команды запуска бота должны отображаться справочная информация и кнопки в клавиатуре(reply Markup):
    # мои товары, добавить товар, помощь, обратиться в поддержку
    # await state.set_state(Form.menu)
    id_user = message.from_user.id
    if not await user_service.get_user(id_user):
        await message.answer("user not exist, adding")
        await user_service.add_user(id_user)
    await message.answer(
        utils.info,
        reply_markup=keyboards.menu_kb,
    )
