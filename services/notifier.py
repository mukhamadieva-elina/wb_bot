from db.product_service import ProductService
from aiogram import Bot


def notify(item_art, new_val: float, product_service: ProductService, bot: Bot):
    positions = product_service.get_users_of_product(item_art)
    for item in positions:
        if item.start_price:
            if item.start_price > new_val:
                bot.send_message(item.user_telegram_id, "Цена понизилась")
            elif item.start_price < new_val:
                bot.send_message(item.user_telegram_id, "Цена повысилась")


def notify_avail(item_art, new_availability, product_service: ProductService, bot: Bot):
    positions = product_service.get_users_of_product(item_art)
    for item in positions:
        if item:
            if new_availability:
                bot.send_message(item.user_telegram_id, "Товар появился в наличии")
            else:
                bot.send_message(item.user_telegram_id, "Товар не в наличии")
