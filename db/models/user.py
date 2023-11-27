from typing import List

from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base



class User(Base):
    __tablename__ = 'User'

    telegram_id: Mapped[int] = mapped_column(primary_key=True, unique=True)

    # Связь с User_Product
    products: Mapped[List["Product"]] = relationship(secondary="User_Product", back_populates="users")

