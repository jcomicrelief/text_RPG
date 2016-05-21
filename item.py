"""ITEM CLASS"""


class Item(object):
    def __init__(self, name, description, value=0, quantity=1):
        self.name = name
        self.raw = name.strip().lower()
        self.description = description
        self.quantity = quantity

        self.value = value
        self.net_value = quantity * value

    # Recalculate value of items
    def recalculate(self):
        self.net_value = self.quantity * self.value
