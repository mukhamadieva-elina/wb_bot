import asyncio

from aiogram import Bot

from api import api_service
from api.api_service import get_image
from api.models.item_info import get_card
from db.product_service import ProductService
from db.user_service import UserService
from services import notifier


def get_price_product_api(api_obj):
    if api_obj:
        price = api_obj[0]['salePriceU'] / 100
        return price


def get_aval_product_api(api_obj):
    if api_obj:
        availability = False
        for size in api_obj[0]['sizes']:
            if len(size['stocks']):
                availability = True
                break
        return availability


async def get_changed_items(product_service: ProductService, user_service: UserService, bot: Bot):
    bd_products = await product_service.get_all_product()
    bd_prod_numbers = [bd_prod.Product.number for bd_prod in bd_products]
    task = [api_service.get_product(product_number) for product_number in bd_prod_numbers]
    api_prods = await asyncio.gather(*task)
    price_changed_items = []
    aval_changed_items = []
    for api_prod, bd_prod in zip(api_prods, bd_products):
        prod_number = bd_prod.Product.number
        bd_prod_price = bd_prod.Product.price
        api_prod_price = get_price_product_api(api_prod)
        bd_prod_aval = bd_prod.Product.availability
        api_prod_aval = get_aval_product_api(api_prod)
        print("bd price:", bd_prod_price)
        print("api price:", api_prod_price)

        if bd_prod_aval != api_prod_aval:
            # await product_service.patch_product(number=prod_number, aval=api_prod_aval)
            aval_changed_items.append((prod_number, api_prod_aval, api_prod_price))
        else:
            if bd_prod_price != api_prod_price:
                if api_prod_aval:
                    print("price_changed_items add")
                    await product_service.patch_product(number=prod_number, price=api_prod_price)
                    price_changed_items.append((prod_number, api_prod_price))

    for (number, api_aval, api_price) in aval_changed_items:
        product = await product_service.get_product(number=number)
        title = product.Product.title
        user_products = await product_service.get_user_products_by_product(number=number)
        for user_product in user_products:
            telegram_id = user_product.UserProduct.user_telegram_id
            start_price = user_product.UserProduct.start_price
            alert_thr = user_product.UserProduct.alert_threshold
            diff = abs(api_price - start_price)
            info, kb = get_card(get_image(number), api_aval, title, start_price, api_price, diff, alert_thr)

            if not api_aval:
                print("мы знаем где мы api aval:", api_aval)
                await bot.send_message(chat_id=telegram_id, text=f"Привет товара больше нет в наличии")
                await bot.send_message(chat_id=telegram_id, text=info, reply_markup=kb(number))
                await product_service.patch_product(number=prod_number, aval=api_aval, price=-1)

            else: # if api_aval == True
                if start_price == -1:
                    await user_service.patch_start_price(api_price)
                    info, kb = get_card(get_image(number), api_aval, title, api_price, api_price, diff, alert_thr)

                await bot.send_message(chat_id=telegram_id, text=f"Привет товар появился в наличии")
                await bot.send_message(chat_id=telegram_id, text=info, reply_markup=kb(number))
                await product_service.patch_product(number=prod_number, aval=api_aval, price=api_price)




    # return price_changed_items, aval_changed_items



    for (number, api_price) in price_changed_items:
        product = await product_service.get_product(number=number)
        product_aval = product.Product.availability
        title = product.Product.title
        user_products = await product_service.get_user_products_by_product(number=number)
        for user_product in user_products:
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



async def update(bot, product_service: ProductService, freq=50):
    print("тут")
    while True:
        products_from_bd = await product_service.get_all_product()  ##продукты из бд
        for product in products_from_bd:
            product_art, product_price, product_avail = product.Product.number, product.Product.price, product.Product.availability
            print(product_art)
            availability_from_api = await check_availability(product_art)
            price_from_api = await check_price_change(product_art)
            if product_price != price_from_api:
                await product_service.patch_product_price(product_art, price_from_api)
                await notifier.notify(product_art, price_from_api, product_service, bot)
            print("ФФЫВУЙКП45СП4Р5ТНРОИАВСЫЧНЕИВПАМВ")
            if product_avail != availability_from_api:
                await product_service.patch_product_availability(product_art, availability_from_api)
                await notifier.notify_avail(product_art, availability_from_api, product_service, bot)
        # time.sleep(freq)
        print("updating")
        await asyncio.sleep(freq)
