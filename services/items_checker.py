from api.api_service import get_product

from db.dto.ProductUpdateDto import ProductUpdateDto
from db.product_service import ProductService

import time

from services import notifier


async def check_price_change(item_art):
    history = await get_product(item_art)
    if history:
        price = history[0]['salePriceU'] / 100
        return price


async def check_availability(item_art):
    history = await get_product(item_art)
    if history:
        availability = False
        for size in history[0]['sizes']:
            if len(size['stocks']):
                availability = True
                break
        return availability


async def update(message, product_service: ProductService, freq=60):
    while True:
        products_from_bd = product_service.get_all_product()  ##продукты из бд
        for product in products_from_bd:
            product_art, product_price, product_avail = product.number, product.price, product.availability
            availability_from_api = await check_availability(product_art)
            price_from_api = await check_price_change(product_art)
            if product_price != price_from_api:
                new_product = ProductUpdateDto(price=price_from_api)
                product_service.patch_product(product_art, new_product)
                notifier.notify(product_art, price_from_api, product_service, message)
            if product_avail != availability_from_api:
                new_product = ProductUpdateDto(availability=availability_from_api)
                product_service.patch_product(product_art, new_product)
                notifier.notify_avail(product_art, availability_from_api, product_service, message)
        time.sleep(freq)
        print("updating")

