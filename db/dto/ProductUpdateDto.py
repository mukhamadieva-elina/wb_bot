class ProductUpdateDto:
    def __init__(self, number=None, title=None, availability=None, price=None):
        self.number = number
        self.title = title
        self.availability = availability
        self.price = price
