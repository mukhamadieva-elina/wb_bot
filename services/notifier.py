from db.product_service import ProductService
from aiogram import Bot


async def notify(item_art, new_val: float, product_service: ProductService, bot: Bot):
    print("notify")
    positions = await product_service.get_users_of_product(item_art)
    print(positions)
    for user_product in positions:
        threshold = user_product.UserProduct.alert_threshold
        if user_product.UserProduct.start_price:
            if (1 + threshold) * user_product.UserProduct.start_price > new_val:
                text = "Цена понизилась на " + str(new_val - user_product.UserProduct.start_price)
                await bot.send_message(user_product.UserProduct.user_telegram_id, text)
            elif user_product.UserProduct.start_price < (1 + threshold) * new_val:
                text = "Цена повысилась на " + str(user_product.UserProduct.start_price - new_val)
                await bot.send_message(user_product.UserProduct.user_telegram_id, text)


async def notify_avail(item_art, new_availability, product_service: ProductService, bot: Bot):
    positions = await product_service.get_users_of_product(item_art)
    for item in positions:
        if item:
            if new_availability:
                await bot.send_message(item.UserProduct.user_telegram_id, "Товар появился в наличии")
            else:
                await bot.send_message(item.UserProduct.user_telegram_id, "Товар не в наличии")