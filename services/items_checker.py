from notifier import Notifier
from typing import TypedDict

class Item(TypedDict):
    art: str
    last_price: int


class ItemsChecker():
    def __int__(self, notifier: Notifier):
        self.items : list[Item] = []
        self.notifier = notifier

    def check_items(self, freq=60*5):
        for item in self.items:
            item_art, last_price = item["art"], item["last_val"]
            new_price = check_price_change(item_art, last_price)
            if new_price:
                self.notifier.notify(item_art, new_price)

    def update(self):
        pass


