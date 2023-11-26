from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Product(Base):
    __tablename__ = 'Product'

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False, unique=True)
    title = Column(String, nullable=False)
    availability = Column(Boolean, nullable=False)
    price = Column(Float, nullable=False)

    # Связь с User_Product
    users = relationship("UserProduct", back_populates="product")
