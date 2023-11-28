from aiogram.utils import keyboard

from api.api_service import get_product, get_image
from api.models import item_info
from api.models.item_info import get_card
from db.product_service import ProductService
from aiogram import Bot

from db.user_service import UserService
from handlers import router


async def notify(item_art, new_val: float, product_service: ProductService, bot: Bot, user_service: UserService):
    print("notify")
    positions = await product_service.get_users_of_product(item_art)
    print(positions)
    if positions:
        for user_product in positions:
            threshold = user_product.UserProduct.alert_threshold
            print(threshold)
            if user_product.UserProduct.start_price:
                if (1 + threshold / 100) * user_product.UserProduct.start_price > new_val:
                    text = "Цена понизилась на " + str(
                        abs(new_val - user_product.UserProduct.start_price)) + "₽. Спешите купить товар! " + "Товар: " + f"https://www.wildberries.ru/catalog/{item_art}/detail.aspx"

                    await bot.send_message(user_product.UserProduct.user_telegram_id, text)
                    product = await user_service.get_user_product_by_number(
                        user_product.UserProduct.user_telegram_id, item_art)
                    info, kb = item_info.get_card(get_image(int(item_art)), product.Product.availability,
                                                  product.Product.title,
                                                  product.UserProduct.start_price,
                                                  product.Product.price,
                                                  abs(product.Product.price - product.UserProduct.start_price),
                                                  product.UserProduct.alert_threshold)
                    await bot.send_message(product.UserProduct.user_telegram_id, info, reply_markup=kb(item_art))

                elif user_product.UserProduct.start_price < (1 + threshold / 100) * new_val:
                    text = "Цена повысилась на " + str(
                        abs(user_product.UserProduct.start_price - new_val)) + "₽. " + "Товар: " + f"https://www.wildberries.ru/catalog/{item_art}/detail.aspx"

                    await bot.send_message(user_product.UserProduct.user_telegram_id, text)
                    product = await user_service.get_user_product_by_number(
                        user_product.UserProduct.user_telegram_id, item_art)
                    info, kb = item_info.get_card(get_image(int(item_art)), product.Product.availability,
                                                  product.Product.title,
                                                  product.UserProduct.start_price,
                                                  product.Product.price,
                                                  abs(product.Product.price - product.UserProduct.start_price),
                                                  product.UserProduct.alert_threshold)
                    await bot.send_message(user_product.UserProduct.user_telegram_id, info, reply_markup=kb(item_art))


async def notify_avail(item_art, new_availability, product_service: ProductService, bot: Bot,
                       user_service: UserService):
    positions = await product_service.get_users_of_product(item_art)

    if positions:
        for item in positions:
            if item:
                if new_availability:
                    text = "Товар появился в наличии, cпешите купить товар! " + "Товар: " + f"https://www.wildberries.ru/catalog/{item_art}/detail.aspx"
                    await bot.send_message(item.UserProduct.user_telegram_id, text)

                    user_product = await user_service.get_user_product_by_number(
                        item.UserProduct.user_telegram_id, item_art)
                    info, kb = item_info.get_card(get_image(int(item_art)), user_product.Product.availability,
                                                  user_product.Product.title,
                                                  user_product.UserProduct.start_price,
                                                  user_product.Product.price,
                                                  abs(user_product.Product.price - user_product.UserProduct.start_price),
                                                  user_product.UserProduct.alert_threshold)
                    await bot.send_message(item.UserProduct.user_telegram_id, info, reply_markup=kb(item_art))
                else:
                    text = "Товар больше не в наличии. " + "Товар: " + f"https://www.wildberries.ru/catalog/{item_art}/detail.aspx"
                    await bot.send_message(item.UserProduct.user_telegram_id, text)
                    user_product = await user_service.get_user_product_by_number(item.UserProduct.user_telegram_id, item_art)
                    info, kb = item_info.get_card(get_image(int(item_art)), new_availability,
                                                  user_product.Product.title,
                                                  user_product.UserProduct.start_price,
                                                  user_product.Product.price,
                                                  abs(user_product.Product.price - user_product.UserProduct.start_price),
                                                  user_product.UserProduct.alert_threshold)
                    await bot.send_message(item.UserProduct.user_telegram_id, info, reply_markup=kb(item_art))
