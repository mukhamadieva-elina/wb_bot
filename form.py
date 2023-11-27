from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    name = State()
    like_bots = State()
    language = State()
    menu = State()
    articul = State()
    support = State()
