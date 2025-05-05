from pyglet import shapes, graphics, text, font, resource, sprite, gui

from logger import log
from cursor import *

class Hud:

    def __init__(self, screen_size, player, window) -> None:
        self.screen_width, self.screen_height = screen_size
        self.player = player
        self.window = window
        self.inventory_open = False
        self.inventory_components = []
        self.inventory_batch = graphics.Batch()
        font.add_file('assets/font/PixelatedElegance.ttf')

        self.hud_components = []
        self.hud_batch = graphics.Batch()

        self.create_hud()

        self.popup_components = []
        self.popup: graphics.Batch = None
        self.popupbatch = graphics.Batch()

    def set_screen_size(self, zoom) -> None:
        self.screen_width /= zoom
        self.screen_height /= zoom

    def create_hud(self) -> None:
        bg = shapes.Rectangle(x=self.screen_height / 32,
                              y=self.screen_height / 32,
                              width=32,
                              height=32,
                              color=(0, 0, 0, 128),
                              batch=self.hud_batch)
        self.hud_components.append(bg)

        current_item = self.player.get_held_item()

        item_img = resource.image(
            f"assets/sprites/item/{current_item['item'].item_id}.png")
        item_sprite = sprite.Sprite(item_img,
                                    x=self.screen_height / 32,
                                    y=self.screen_height / 32,
                                    batch=self.hud_batch)
        item_sprite.scale = 2.0
        self.hud_components.append(item_sprite)

    def create_inventory(self) -> None:
        bg = shapes.Rectangle(x=self.screen_height / 16,
                              y=self.screen_height / 16,
                              width=0.4 * self.screen_width,
                              height=self.screen_height * 0.875,
                              color=(0, 0, 0, 128),
                              batch=self.inventory_batch)
        self.inventory_components.append(bg)

        title = text.Label('Inventory',
                           font_name="Pixelated Elegance",
                           font_size=0.03125 * self.screen_width,
                           x=self.screen_height * 0.09375,
                           y=self.screen_height - 48,
                           anchor_x='left',
                           anchor_y='top',
                           batch=self.inventory_batch)
        self.inventory_components.append(title)

        for i, item in enumerate(self.player.inventory):
            item_text = text.Label(
                f"{item['item'].display_name} x{item['count']}",
                font_name="Pixelated Elegance",
                font_size=12,
                x=48,
                y=(self.screen_height - (i * 16) - 96),
                anchor_x='left',
                anchor_y='top',
                batch=self.inventory_batch)
            self.inventory_components.append(item_text)

    def open_inventory(self) -> None:
        self.create_inventory()
        self.inventory_open = True

    def close_inventory(self) -> None:
        for i in self.inventory_components:
            i.batch = None
        self.inventory_open = False
    
    def create_popup(self, gid, x, y, w, h,player) -> None:
        self.close_popup(player)
        player.can_move=False
        x = self.screen_width / 2 - 128
        y = self.screen_height / 2 - 64

        widnow = shapes.RoundedRectangle(x=x,
                                         y=y,
                                         width=w,
                                         height=h,
                                         radius=9,
                                         color=(122, 118, 156, 176),
                                         batch=self.popupbatch)

        border0 = shapes.Line(x=(x + 16),
                              y=(y + h - 1),
                              x2=(x + w - 16),
                              y2=(y + h - 1),
                              color=(34, 32, 52),
                              batch=self.popupbatch)
        border1 = shapes.Line(x=(x + w),
                              y=(y + h - 16),
                              x2=(x + w),
                              y2=(y + 16),
                              color=(34, 32, 52),
                              batch=self.popupbatch)
        border2 = shapes.Line(x=(x + 16),
                              y=(y),
                              x2=(x + w - 16),
                              y2=(y),
                              color=(34, 32, 52),
                              batch=self.popupbatch)
        border3 = shapes.Line(x=(x + 1),
                              y=(y + 16),
                              x2=(x + 1),
                              y2=(y + h - 16),
                              color=(34, 32, 52),
                              batch=self.popupbatch)

        corners = resource.image("assets/sprites/hud/popup_corners.png")

        corner0 = sprite.Sprite(corners.get_region(0, 0, 16, 16),
                                x=x,
                                y=y,
                                batch=self.popupbatch)
        corner1 = sprite.Sprite(corners.get_region(16, 0, 16, 16),
                                x=x + w - 16,
                                y=y,
                                batch=self.popupbatch)
        corner2 = sprite.Sprite(corners.get_region(0, 16, 16, 16),
                                x=x,
                                y=y + h - 16,
                                batch=self.popupbatch)
        corner3 = sprite.Sprite(corners.get_region(16, 16, 16, 16),
                                x=x + w - 16,
                                y=y + h - 16,
                                batch=self.popupbatch)

        pressed = resource.image("assets/sprites/item/1.png")
        unpressed = resource.image("assets/sprites/hud/close.bmp")
        close_btn = gui.PushButton(x=x + w - 16,
                                   y=y + h - 16,
                                   pressed=pressed,
                                   unpressed=unpressed,
                                   batch=self.popupbatch)
        self.window.push_handlers(close_btn)

        def on_press(_) -> None:
            self.close_popup(player)

        close_btn.set_handler('on_press', on_press)
        self.popup_components.extend([
            border0, border1, border2, border3, corner0, corner1, corner2,
            corner3, widnow, close_btn
        ])

        self.popup = self.popupbatch

    def getpopupbatch(self):
        return self.popupbatch, self.popup_components

    def close_popup(self,player) -> None:
        self.popup_components.clear()
        player.can_move = True
        self.popup = None
        
    
    


        
