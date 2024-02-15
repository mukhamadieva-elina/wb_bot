from typing import Callable, Any, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from wb_bot.db.product_service import ProductService
from wb_bot.db.user_service import UserService


class CounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        self.counter += 1
        data['counter'] = self.counter
        return await handler(event, data)

class ServiceMiddleware(BaseMiddleware):
    def __init__(self, engine) -> None:
        self.product_service = ProductService(engine)
        self.user_service = UserService(engine)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        data['product_service'] = self.product_service
        data['user_service'] = self.user_service
        return await handler(event, data)