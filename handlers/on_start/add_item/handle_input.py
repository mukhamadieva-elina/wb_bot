# При нажатии на кнопку “Добавить товар” бот присылает сообщение с просьбой отправить артикул товара.
# Также появляется кнопка в клавиатуре “Назад” (при нажатии на которую бот возвращается в главное меню)
# Хендлер, который срабатывает на добавить товар.
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import keyboards
import utils
from form import Form

add_item_router = Router()


@add_item_router.message(Form.articul)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(articul=message.text)

    if utils.validateArticul():
        if utils.existInAPI():
            await state.set_state(Form.menu)
            if utils.item_in_bd():
                if utils.user_already_have_its_item():
                    await message.answer(f"есть такой артикул!")
                else:
                    await message.answer(f"Товар успешно добавлен!")
                    # прислать карточку
                    # успешно выйти в главное меню
            else:
                await message.answer(f"Товар успешно добавлен!")
                # прислать карточку
                # успешно выйти в главное меню
        else:
            await state.set_state(Form.articul)
            await message.answer(f"Товара не существует попробуйте снова!",
                                 reply_markup=keyboards.return_to_menu_kb)
    # товара не существует попробуйте снова (снова кнопку назад делаем)
    else:
        await state.set_state(Form.articul)
        await message.answer(f"Артикул некорректен, попробуйте снова!",
                             reply_markup=keyboards.return_to_menu_kb)
    # Артикул некорректнет, попробуйте снова (снова кнопку назад делаем)
