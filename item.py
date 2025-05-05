import json as json

class Item:
    def __init__(self, item_id, display_name) -> None:
        self.item_id = item_id
        self.display_name = display_name

            
CHEESE = Item(0, 'Cheese')
MUG = Item(1, 'Mug')