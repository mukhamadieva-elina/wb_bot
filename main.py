import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

import config

import handlers
from api import api_service
from db.models.base import Base
from middleware.service_middleware import ServiceMiddleware
from services import items_checker

TOKEN = config.TOKEN

# DATABASE_URL = f"postgresql+asyncpg://dyvawvhc:{config.bd_pass}@trumpet.db.elephantsql.com/dyvawvhc"
DATABASE_URL = f"postgresql+asyncpg://nusiykxb:{config.bd_pass}@lucky.db.elephantsql.com/nusiykxb"

engine = create_async_engine(DATABASE_URL)

service_middleware = ServiceMiddleware(engine)
handlers.router.message.middleware(service_middleware)
handlers.router.callback_query.middleware(service_middleware)
product_service = service_middleware.product_service
user_service = service_middleware.user_service

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# items_checker.getChangedItems(product_service)

async def regular_update():

    # products = await product_service.get_all_product()
    # print(products)
    while True:
        await items_checker.get_changed_items(product_service, user_service, bot)
        await asyncio.sleep(10)

    # await items_checker.update(bot, product_service)



async def main():

    dp.include_routers(handlers.router)


    task = asyncio.create_task(regular_update())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
