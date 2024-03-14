from aiogram import Bot
from aiogram.enums import ParseMode

import config

TOKEN = config.TOKEN

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
