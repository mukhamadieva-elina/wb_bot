from db.product_service import ProductService
from aiogram import Bot

from handlers import router


async def notify(item_art, new_val: float, product_service: ProductService, bot: Bot):
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

                elif user_product.UserProduct.start_price < (1 + threshold / 100) * new_val:
                    text = "Цена повысилась на " + str(
                        abs(user_product.UserProduct.start_price - new_val)) + "₽" + "товар: " + f"https://www.wildberries.ru/catalog/{item_art}/detail.aspx"

                    await bot.send_message(user_product.UserProduct.user_telegram_id, text)


async def notify_avail(item_art, new_availability, product_service: ProductService, bot: Bot):
    positions = await product_service.get_users_of_product(item_art)
    if positions:
        for item in positions:
            if item:
                if new_availability:
                    text = "Товар появился в наличии, cпешите купить товар! " + "Товар: " + f"https://www.wildberries.ru/catalog/{item_art}/detail.aspx"
                    await bot.send_message(item.UserProduct.user_telegram_id, text)
                else:
                    text = "Товар больше не в наличии. " + "Товар: " + f"https://www.wildberries.ru/catalog/{item_art}/detail.aspx"
                    await bot.send_message(item.UserProduct.user_telegram_id, text)
