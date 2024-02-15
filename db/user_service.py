from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, Session

from db.models import User, Product, UserProduct
from db.product_service import ProductService
from db.utils import session_decorator_nested, session_decorator


class UserService:

    def __init__(self, engine):
        self.session = sessionmaker(bind=engine, class_=AsyncSession)

    @session_decorator
    async def get_user(self, telegram_id, session: Session):
        query = select(User).filter_by(telegram_id=telegram_id)
        result = await session.execute(query)
        return result.first()
        # return session.query(User).filter_by(telegram_id=telegram_id).first()

    @session_decorator
    async def add_user(self, telegram_id, session: Session):
        inserting_user = insert(User).values(telegram_id=telegram_id)
        await session.execute(inserting_user)

    @session_decorator
    async def get_user_products(self, telegram_id: int, session: Session):
        query = select(Product, UserProduct).join(UserProduct, UserProduct.product_id == Product.id) \
            .filter(UserProduct.user_telegram_id == telegram_id)
        result = await session.execute(query)
        products = result.all()

        session.expunge_all()
        return products

    @session_decorator
    async def get_user_product_by_number(self, telegram_id: int, number: int, session: Session):
        query = select(Product, UserProduct).join(UserProduct, UserProduct.product_id == Product.id) \
            .filter(UserProduct.user_telegram_id == telegram_id).filter(Product.number == number)
        result = await session.execute(query)
        product = result.first()
        session.expunge_all()
        return product

    @session_decorator
    async def user_product_exists_by_number(self, telegram_id: int, number: int, session: Session):
        query = select(Product).join(UserProduct).filter(UserProduct.user_telegram_id == telegram_id). \
            filter(Product.number == number)
        result = await session.execute(query)
        product = result.all()
        return True if product else False

    @session_decorator
    async def delete_user_product(self, telegram_id, product_number, session: Session):
        query = select(UserProduct).filter_by(user_telegram_id=telegram_id).join(Product).filter_by(
            number=product_number)
        result = await session.execute(query)
        user_product = result.first()
        if user_product:
            await session.delete(user_product.UserProduct)
            # await session.commit() должен итак примениться надеюсь

    @session_decorator
    async def patch_alert_threshold(self, telegram_id, product_number, alert_threshold: int, session: Session):
        query = select(Product).filter_by(number=product_number)
        result = await session.execute(query)
        product = result.first()
        query = select(UserProduct).filter_by(user_telegram_id=telegram_id, product_id=product.Product.id)
        result = await session.execute(query)
        user_product = result.first()
        if user_product:
            user_product.UserProduct.alert_threshold = alert_threshold
            # session.commit()

    @session_decorator
    async def patch_start_price(self, telegram_id, product_number, session: Session):
        query = select(Product).filter_by(number=product_number)
        result = await session.execute(query)
        product = result.first()

        query = select(UserProduct).filter_by(user_telegram_id=telegram_id, product_id=product.Product.id)
        result = await session.execute(query)
        user_product = result.first()
        if user_product:
            user_product.UserProduct.start_price = product.Product.price

    @session_decorator_nested
    async def add_user_product(self, telegram_id, number, product_service: ProductService, session: Session):
        # if not product_service.product_exists_by_number(product.number):
        #     product_service.add_product(product)
        product = await product_service.get_product(number)
        inserting_user = insert(UserProduct).values(user_telegram_id=telegram_id, product_id=product.Product.id,
                                                    start_price=product.Product.price, alert_threshold=0)
        await session.execute(inserting_user)
