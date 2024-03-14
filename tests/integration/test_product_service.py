import pytest

from db.models import Product
from db.product_service import ProductService
from sqlalchemy import insert, select, delete, update


@pytest.mark.asyncio
async def test_patch_start_price(connection):
    product = {'id': 5, 'number': 123, 'title': '1', 'availability': True, 'price': 100}
    product_service = ProductService(connection)
    session = product_service.session

    async with connection.connect() as conn:
        await conn.execute(insert(Product).values(id=product['id'], number=product['number'], title=product['title'],
                                                  availability=product['availability'], price=product['price']))

        await conn.commit()
        new_availability = not product['availability']
        new_price = product['price'] + 1
        await product_service.patch_product(session=session, number=product['number'], price=new_price,
                                            aval=new_availability)
        result = await conn.execute(select(Product).filter_by(id=product['id']))
        await conn.execute(delete(Product).where(Product.id == product['id']))
        await conn.commit()
        assert result.first().price == new_price

@pytest.mark.asyncio
async def test_add_product(connection):
    product = {'id': 1000, 'number': 1230, 'title': '1', 'availability': True, 'price': 100}
    product_service = ProductService(connection)
    async with connection.connect() as conn:
        await conn.execute(insert(Product).values(id=product['id'], number=product['number'], title=product['title'],
                                                  availability=product['availability'], price=product['price']))
        await conn.commit()
        await product_service.add_product(number=product['number'], title=product['title'],
                                          availability=product['availability'], price=product['price'], session=conn)
        result = await conn.execute(select(Product.id).filter_by(number=product['number']))
        if result:
            await conn.execute(delete(Product).where(Product.number == product['number']))
            await conn.commit()
        rowcount = result.rowcount
        assert rowcount == 1