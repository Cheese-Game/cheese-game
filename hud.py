from pyglet import shapes, graphics, text, font

from logger import log


class Hud:
    def __init__(self, screen_size, player) -> None:
        self.screen_width, self.screen_height = screen_size
        self.player = player

        self.inventory_open = False
        self.inventory_components = []
        self.inventory_batch = graphics.Batch()

        font.add_file('assets/font/PixelatedElegance.ttf')

        self.create_inventory()

    def create_inventory(self) -> None:
        bg = shapes.Rectangle(x=32, y=32, width=256, height=416, color=(0, 0, 0, 128), batch=self.inventory_batch)
        self.inventory_components.append(bg)

        title = text.Label('Inventory',
                           font_name="Pixelated Elegance", font_size=18,
                           x=48, y=self.screen_height-48, anchor_x='left', anchor_y='top',
                           batch=self.inventory_batch)
        self.inventory_components.append(title)

        for i, item in enumerate(self.player.inventory):
            item_text = text.Label(f"{item['item'].display_name} x{item['count']}",
                                   font_name="Pixelated Elegance", font_size=12,
                                   x=48, y=(self.screen_height - (i * 16) - 96), anchor_x='left', anchor_y='top',
                                   batch=self.inventory_batch)
            self.inventory_components.append(item_text)

    def open_inventory(self) -> None:
        log("Inventory opened")
        self.inventory_open = True

    def close_inventory(self) -> None:
        log("Inventory closed")
        self.inventory_open = False
