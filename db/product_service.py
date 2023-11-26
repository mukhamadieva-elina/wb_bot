from sqlalchemy.orm import sessionmaker, Session

from db.dto.ProductUpdateDto import ProductUpdateDto
from db.models.product import Product
from db.utils import session_decorator, session_decorator_nested


class ProductService:

    def __init__(self, engine):
        self.session = sessionmaker(bind=engine)
    @session_decorator
    def product_exists_by_number(self, number, session):
        product = session.query(Product).filter_by(number=number).first()
        return product is not None

    @session_decorator_nested
    def get_product(self, number, session: Session):
        return session.query(Product).filter_by(number=number).first()
    @session_decorator_nested
    def patch_product(self, number, product_update: ProductUpdateDto, session):
        # product = session.query(Product).filter_by(number=number).first()
        product = self.get_product(number, session=session)
        if not product:
            raise Exception
        for attr in vars(product_update).keys():
            value = getattr(product_update, attr)
            print("value", value)
            if value is not None:
                setattr(product, attr, value)