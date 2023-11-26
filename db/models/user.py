from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = 'User'

    telegram_id = Column(Integer, primary_key=True, unique=True)
    user_name = Column(String, nullable=False)

    # Связь с User_Product
    products = relationship("UserProduct", back_populates="user")
