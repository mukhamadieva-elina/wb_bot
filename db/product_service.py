from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, Session

from db.dto.ProductUpdateDto import ProductUpdateDto
from db.models.product import Product
from db.models.user_product import UserProduct
from db.utils import session_decorator, session_decorator_nested


class ProductService:

    def __init__(self, engine):
        self.session = sessionmaker(bind=engine, class_=AsyncSession)

    @session_decorator
    async def product_exists_by_number(self, number, session):
        query = select(Product).filter_by(number=number)
        result = await session.execute(query)
        product = result.first()
        return product is not None

    @session_decorator
    async def get_product(self, number, session: Session):
        query = select(Product).filter_by(number=number)
        result = await session.execute(query)
        product = result.first()
        session.expunge_all()
        return product

    @session_decorator_nested
    async def patch_product(self, number, product_update: ProductUpdateDto, session):
        print("patch")
        # product = session.query(Product).filter_by(number=number).first()
        product = await self.get_product(number, session=session)
        if not product:
            raise Exception
        for attr in vars(product_update).keys():
            value = getattr(product_update, attr)
            print("value", value)
            if value is not None:
                setattr(product, attr, value)

    @session_decorator
    async def add_product(self, number, title, availability, price, session: Session):
        if not await self.product_exists_by_number(number):
            inserting_product = insert(Product).values(number=number, title=title, availability=availability,
                                                       price=price)
            await session.execute(inserting_product)

    @session_decorator_nested
    async def get_all_product(self, session: Session):
        query = select(Product)
        result = await session.execute(query)
        products = result.all()
        session.expunge_all()
        return products

    @session_decorator
    async def get_users_of_product(self, number, session: Session):
        print("lknkjn")
        query = select(UserProduct).join(Product).filter_by(number=number)
        result = await session.execute(query)
        user_products = result.all()
        session.expunge_all()
        print(user_products)
        return user_products