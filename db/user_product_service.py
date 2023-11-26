from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker, Session
from db.models.product import Product
from db.models.user_product import UserProduct
from db.product_service import ProductService
from db.utils import session_decorator, session_decorator_nested


class UserProductService:

    def __init__(self, engine):
        self.session = sessionmaker(bind=engine)

    @session_decorator
    def get_user_products(self, telegram_id: int, session: Session):
        products = session.query(Product, UserProduct).join(UserProduct, UserProduct.product_id == Product.id) \
            .filter(UserProduct.user_telegram_id == telegram_id).all()
        session.expunge_all()
        return products

    @session_decorator
    def get_user_product_by_number(self, telegram_id: int, number: int, session: Session):
        product = session.query(Product, UserProduct).join(UserProduct, UserProduct.product_id == Product.id) \
            .filter(UserProduct.user_telegram_id == telegram_id).filter(Product.number == number).first()
        session.expunge_all()
        return product

    @session_decorator
    def user_product_exists_by_number(self, telegram_id: int, number: int, session: Session):
        product = session.query(Product).join(UserProduct).filter(UserProduct.user_telegram_id == telegram_id). \
            filter(Product.number == number).all()
        return True if product else False

    @session_decorator_nested
    def delete_user_product(self, telegram_id, product_number, session: Session):
        user_product = session.query(UserProduct).filter_by(user_telegram_id=telegram_id).join(Product).filter_by(
            number=product_number).first()
        if user_product:
            session.delete(user_product)
            session.commit()

    @session_decorator_nested
    def patch_alert_threshold(self, telegram_id, product_number, alert_threshold: int, session: Session):
        product = session.query(Product).filter_by(number=product_number).first()
        user_product = session.query(UserProduct).filter_by(user_telegram_id=telegram_id, product_id=product.id)
        if user_product:
            user_product.update({"alert_threshold": alert_threshold})
            session.commit()

    @session_decorator_nested
    def patch_start_price(self, telegram_id, product_number, session: Session):
        product = session.query(Product).filter_by(number=product_number).first()
        user_product = session.query(UserProduct).filter_by(user_telegram_id=telegram_id, product_id=product.id)
        if user_product:
            user_product.update({"start_price": product.price})
            session.commit()

    @session_decorator
    def add_user_product(self, telegram_id, number, product_service: ProductService, session: Session):
        # if not product_service.product_exists_by_number(product.number):
        #     product_service.add_product(product)
        product = product_service.get_product(number)
        inserting_user = insert(UserProduct).values(user_telegram_id=telegram_id, product_id=product.id,
                                                    start_price=product.price, alert_threshold=0)
        session.execute(inserting_user)