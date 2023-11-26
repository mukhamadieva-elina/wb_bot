from typing import List

from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base


class UserProduct(Base):
    __tablename__ = 'User_Product'

    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('User.telegram_id'), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('Product.id'), primary_key=True)
    start_price: Mapped[float] = mapped_column(nullable=False)
    alert_threshold: Mapped[int] = mapped_column(nullable=False)