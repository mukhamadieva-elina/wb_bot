from typing import List

from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm import Mapped
from .base import Base


class Product(Base):
    __tablename__ = 'Product'

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(nullable=False, unique=True)
    title: Mapped[str] = mapped_column(nullable=False)
    availability: Mapped[bool] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    users: Mapped[List["User"]] = relationship(secondary="User_Product", back_populates="products")
