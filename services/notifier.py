
from typing import TypedDict


class UserItem(TypedDict):
    telegram_id: str
    last_price: int

class Notifier():
    def __int__(self):
        pass

    def update(self):
        print(1)

    def notify(self, item_art, new_val):
        pass


