import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

import config

import handlers
from api import api_service
from middleware.service_middleware import ServiceMiddleware
from services import items_checker

TOKEN = config.TOKEN

DATABASE_URL = f"postgresql+asyncpg://dyvawvhc:{config.bd_pass}@trumpet.db.elephantsql.com/dyvawvhc"

engine = create_async_engine(DATABASE_URL)

service_middleware = ServiceMiddleware(engine)
handlers.router.message.middleware(service_middleware)
handlers.router.callback_query.middleware(service_middleware)
product_service = service_middleware.product_service

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


async def regular_update():
    i = 0
    while True:
        print(f"main")
        await items_checker.update(bot, product_service)


async def main():
    dp.include_routers(handlers.router)
    task = asyncio.create_task(regular_update())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
