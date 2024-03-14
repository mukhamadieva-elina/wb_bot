import asyncio

from api.api_service import get_image
from api.models.item_info import get_card
from db.product_service import ProductService
from aiogram import Bot

from db.user_service import UserService
from services.items_checker import get_changed_items


async def notify_aval(aval_changed_items, product_service: ProductService, user_service: UserService, bot: Bot):
    async def notify_aval_user(user_product):
        telegram_id = user_product.UserProduct.user_telegram_id
        start_price = user_product.UserProduct.start_price
        alert_thr = user_product.UserProduct.alert_threshold
        diff = abs(api_price - start_price)
        info, kb = get_card(get_image(number), api_aval, title, start_price, api_price, diff, alert_thr)

        if not api_aval:
            print("мы знаем где мы api aval:", api_aval)
            await bot.send_message(chat_id=telegram_id, text=f"Привет товара больше нет в наличии")
            await bot.send_message(chat_id=telegram_id, text=info, reply_markup=kb(number))
            await product_service.patch_product(number=number, aval=api_aval, price=-1)

        else:  # if api_aval == True
            if start_price == -1:
                await user_service.patch_start_price(telegram_id, number)
                info, kb = get_card(get_image(number), api_aval, title, api_price, api_price, 0, alert_thr)

            await bot.send_message(chat_id=telegram_id, text=f"Привет товар появился в наличии")
            await bot.send_message(chat_id=telegram_id, text=info, reply_markup=kb(number))
            await product_service.patch_product(number=number, aval=api_aval, price=api_price)


    for (number, api_aval, api_price) in aval_changed_items:
        print("number:", number)
        product = await product_service.get_product(number=number)
        title = product.Product.title
        user_products = await product_service.get_user_products_by_product(number=number)
        task = [notify_aval_user(user_product) for user_product in user_products]
        print("aval gather")
        await asyncio.gather(*task)
        print("after aval gather")



async def notify_prices(price_changed_items, product_service: ProductService, bot: Bot):
    async def notify_price_user(user_product):
        telegram_id = user_product.UserProduct.user_telegram_id
        start_price = user_product.UserProduct.start_price
        alert_thr = user_product.UserProduct.alert_threshold
        diff = abs(api_price - start_price)

        info, kb = get_card(get_image(number), product_aval, title, start_price, api_price, diff, alert_thr)
        if api_price > (1 + alert_thr / 100) * start_price:
            await bot.send_message(chat_id=telegram_id, text=f"Привет цена увеличилась на {diff}")
            await bot.send_message(chat_id=telegram_id, text=info, reply_markup=kb(number))
        elif api_price < (1 - alert_thr / 100) * start_price:
            await bot.send_message(chat_id=telegram_id, text=f"Привет цена уменьшилась на {diff}")
            await bot.send_message(chat_id=telegram_id, text=info, reply_markup=kb(number))

    for (number, api_price) in price_changed_items:
        product = await product_service.get_product(number=number)
        product_aval = product.Product.availability
        title = product.Product.title
        user_products = await product_service.get_user_products_by_product(number=number)
        task = [notify_price_user(user_product) for user_product in user_products]
        await asyncio.gather(*task)



async def run(product_service: ProductService, user_serivce: UserService, bot):
    print("NOTIFIER RUN:")
    aval_items, price_items = await get_changed_items(product_service)
    print("get chaned items end")
    await notify_aval(aval_items, product_service, user_serivce, bot)
    print("notify_aval")
    await notify_prices(price_items, product_service, bot)
    print("notify prices")
