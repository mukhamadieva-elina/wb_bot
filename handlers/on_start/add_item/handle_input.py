# При нажатии на кнопку “Добавить товар” бот присылает сообщение с просьбой отправить артикул товара.
# Также появляется кнопка в клавиатуре “Назад” (при нажатии на которую бот возвращается в главное меню)
# Хендлер, который срабатывает на добавить товар.
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hide_link

import keyboards
import utils
from db.models.product import Product
from db.product_service import ProductService
from db.user_service import UserService
from form import Form
from api import api_service
from api.models.item_info import get_card

from handlers.router import router


@router.message(Form.articul)
async def process_name(message: Message, state: FSMContext, product_service: ProductService,
                       user_service: UserService) -> None:
    number = message.text
    user_id = message.from_user.id
    await state.update_data(articul=number)
    if utils.validate_articul(number):
        number = int(number)
        exists = await utils.exist_in_api(number)
        if exists:
            await state.set_state(Form.menu)
            product = product_service.get_product(number)
            if product:
                if user_service.user_product_exists_by_number(user_id, product.number):
                    await message.answer(f"Вы уже отслеживаете этот товар!", reply_markup=keyboards.menu_kb)
                else:
                    user_service.add_user_product(user_id, number, product_service)
                    await message.answer(f"Товар успешно добавлен!", reply_markup=keyboards.menu_kb)
                    info, kb = get_card(api_service.get_image(int(number)), product.availability, product.title,
                                        product.price, product.price, 0, 0)
                    await message.answer(
                        info,
                        reply_markup=kb(number)
                    )
                    # прислать карточку
                    # успешно выйти в главное меню
            else:
                product_from_api = await api_service.get_product(number)
                availability = False
                for size in product_from_api[0]['sizes']:
                    if len(size['stocks']):
                        availability = True
                        break
                product_service.add_product(number, product_from_api[0]['name'], availability,
                                            product_from_api[0]['salePriceU'] / 100)
                user_service.add_user_product(user_id, number, product_service)
                await message.answer(f"Товар успешно добавлен!")
                info, kb = get_card(api_service.get_image(int(number)), availability, product_from_api[0]['name'],
                                    product_from_api[0]['salePriceU'] / 100,
                                    product_from_api[0]['salePriceU'] / 100, 0, 0)
                await message.answer(
                    info,
                    reply_markup=kb(number)
                )
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
