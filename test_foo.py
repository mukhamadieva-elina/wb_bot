import pytest
from sqlalchemy import insert, select, delete, Result
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import test_bd_pass
from db.models import Product

@pytest.mark.asyncio
async def test_patch_start_price():
    engine = create_async_engine(
        f"postgresql+asyncpg://dyvawvhc:{test_bd_pass}@trumpet.db.elephantsql.com/dyvawvhc"
    )
    session = async_sessionmaker(engine)

    product = {'id': 5, 'number': 123, 'title': '1', 'availability': True, 'price': 100}

    async with session.begin() as conn:
        await conn.execute(insert(Product).values(id=product['id'], number=product['number'], title=product['title'],
                                                  availability=product['availability'], price=product['price']))

        result = await conn.execute(select(Product).filter_by(id=product['id']))
        await conn.execute(delete(Product).where(Product.id == product['id']))




#
@pytest.mark.asyncio
async def test_add_product():
    engine = create_async_engine(
        f"postgresql+asyncpg://dyvawvhc:{test_bd_pass}@trumpet.db.elephantsql.com/dyvawvhc"
    )
    session = async_sessionmaker(engine)

    product = {'id': 1000, 'number': 1230, 'title': '1', 'availability': True, 'price': 100}

    async with session.begin() as conn:
        assert 2 == 2
        result: Result = await conn.execute(select(Product.id).filter_by(number=product['number']))


