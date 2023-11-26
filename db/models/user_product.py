from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
class UserProduct(Base):
    __tablename__ = 'User_Product'

    user_telegram_id = Column(Integer, ForeignKey('User.telegram_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('Product.id'), primary_key=True)
    start_price = Column(Float, nullable=False)
    alert_threshold = Column(Integer, nullable=False)

    # Определение связей с таблицами User и Product
    user = relationship("User", back_populates="products")
    product = relationship("Product", back_populates="users")