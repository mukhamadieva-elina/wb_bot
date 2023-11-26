#При нажатии на кнопку “Добавить товар” бот присылает сообщение с просьбой отправить артикул товара.
# Также появляется кнопка в клавиатуре “Назад” (при нажатии на которую бот возвращается в главное меню)
# Хендлер, который срабатывает на добавить товар.
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

class Form(StatesGroup):
    articul_input = State()


add_item_router = Router()

@add_item_router.message(F.text.casefold() == "q")
async def hello(message: Message, state: FSMContext):
    await state.set_state(Form.articul_input)
    #Просим отправить артикул товара, рисуем кнопку назад
    await message.reply("Hello! How can I help you today?")


@add_item_router.message(Form.articul_input)
async def process_name(message: Message, state: FSMContext) -> None:
    if validateArticul():
        if existInAPI():
            if item_in_bd():
                if user_already_have_its_item():
                    write_about_that
                else:
                    add_user_item_bd(last_price)
                    #прислать карточку
                    #успешно выйти в главное меню
            else:
                add_item_in_bd()
                add_user_item_bd(last_price)
                #прислать карточку
                # успешно выйти в главное меню
        else:
            #товара не существует попробуйте снова (снова кнопку назад делаем)
    else:
        #Артикул некорректнет, попробуйте снова (снова кнопку назад делаем)




    await state.clear()
