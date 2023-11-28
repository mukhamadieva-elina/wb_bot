import asyncio
from api import api_service
from db.product_service import ProductService

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


async def get_changed_items(product_service: ProductService):
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

        if bd_prod_aval != api_prod_aval:
            aval_changed_items.append((prod_number, api_prod_aval, api_prod_price))
        else:
            if bd_prod_price != api_prod_price:
                if api_prod_aval:
                    print("price_changed_items add")
                    await product_service.patch_product(number=prod_number, price=api_prod_price)
                    price_changed_items.append((prod_number, api_prod_price))

    return aval_changed_items, price_changed_items

