from pyglet import shapes, graphics, text, font, resource, sprite

from logger import log


class Hud:
    def __init__(self, screen_size, player) -> None:
        self.screen_width, self.screen_height = screen_size
        self.player = player

        self.inventory_open = False
        self.inventory_components = []
        self.inventory_batch = graphics.Batch()

        font.add_file('assets/font/PixelatedElegance.ttf')

        self.hud_components = []
        self.hud_batch = graphics.Batch()

        self.create_hud()

    def set_screen_size(self, zoom) -> None:
        self.screen_width = self.screen_width / zoom
        self.screen_height = self.screen_height / zoom

    def create_hud(self) -> None:
        
        bg = shapes.Rectangle(x=self.screen_height/16, y=self.screen_height/16, width=64, height=64, color=(0, 0, 0, 128), batch=self.hud_batch)
        self.hud_components.append(bg)

        current_item = self.player.get_held_item()

        item_img = resource.image(f"assets/sprites/item/{current_item['item'].item_id}.png")
        item_sprite = sprite.Sprite(item_img, x=self.screen_height/16, y=self.screen_height/16, batch=self.hud_batch)
        item_sprite.scale = 4.0
        self.hud_components.append(item_sprite)

        

    def create_inventory(self) -> None:
        bg = shapes.Rectangle(x=self.screen_height/16, y=self.screen_height/16, width=0.4*self.screen_width, height=self.screen_height*0.875, color=(0, 0, 0, 128), batch=self.inventory_batch)
        self.inventory_components.append(bg)

        title = text.Label('Inventory',
                           font_name="Pixelated Elegance", font_size=0.03125*self.screen_width,
                           x=self.screen_height*0.09375, y=self.screen_height-48, anchor_x='left', anchor_y='top',
                           batch=self.inventory_batch)
        self.inventory_components.append(title)

        for i, item in enumerate(self.player.inventory):
            item_text = text.Label(f"{item['item'].display_name} x{item['count']}",
                                   font_name="Pixelated Elegance", font_size=12,
                                   x=48, y=(self.screen_height - (i * 16) - 96), anchor_x='left', anchor_y='top',
                                   batch=self.inventory_batch)
            self.inventory_components.append(item_text)

    def open_inventory(self) -> None:
        self.create_inventory()
        self.inventory_open = True

    def close_inventory(self) -> None:
        for i in self.inventory_components:
            i.batch = None
        self.inventory_open = False
