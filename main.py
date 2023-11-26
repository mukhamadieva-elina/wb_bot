import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

import config
from handlers.on_start.add_item.handle_input import add_item_router
from handlers.on_start.add_item.input_item import input_item_router
from handlers.on_start.add_item.back import back_from_add_item
from handlers.on_start.items.change_notify.change_notify import update_treshhold_router
from handlers.on_start.items.change_notify.change_notify_options import update_treshhold_options_router
from handlers.on_start.items.change_price_to_last import change_price_router
from handlers.on_start.items.items import my_items_router
from handlers.on_start.items.price_diagram.price_diagram import price_diagram_router
from handlers.on_start.items.stop_tracking import stop_tracking_router
from handlers.start import on_start_router

TOKEN = config.TOKEN
print(TOKEN)


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(on_start_router, my_items_router, input_item_router, back_from_add_item,
                       stop_tracking_router, add_item_router, change_price_router, update_treshhold_router,
                       update_treshhold_options_router, price_diagram_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
