from pyglet import shapes, graphics, text, font, resource, sprite, gui

from logger import log, warn
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

        self.dialog_components = []
        self.dialog: graphics.Batch = None
        self.dialog_contents: graphics.Batch = None
        self.dialog_batch = graphics.Batch()

        self.active_gui_components = []

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
        self.active_gui_components.append(self.inventory_batch)

    def close_inventory(self) -> None:
        for i in self.inventory_components:
            i.batch = None
        self.inventory_open = False
        self.active_gui_components.remove(self.inventory_batch)
    
    def create_dialog(self, x, y, w, h, player, dialog_contents: list) -> None:
        self.close_dialog(player)
        log("opening dialog")
        self.dialog_contents = dialog_contents
        player.can_move=False
        #x = self.screen_width / 2 - 128
        #y = self.screen_height / 2 - 64

        widnow = shapes.RoundedRectangle(x=x, y=y, width=w, height=h,
                                         radius=9, color=(122, 118, 156, 176),
                                         batch=self.dialog_batch)

        border0 = shapes.Line(x=(x + 16), y=(y + h - 1),
                              x2=(x + w - 16), y2=(y + h - 1),
                              color=(34, 32, 52), batch=self.dialog_batch)
        border1 = shapes.Line(x=(x + w), y=(y + h - 16),
                              x2=(x + w), y2=(y + 16),
                              color=(34, 32, 52), batch=self.dialog_batch)
        border2 = shapes.Line(x=(x + 16), y=(y),
                              x2=(x + w - 16), y2=(y),
                              color=(34, 32, 52), batch=self.dialog_batch)
        border3 = shapes.Line(x=(x + 1), y=(y + 16),
                              x2=(x + 1), y2=(y + h - 16),
                              color=(34, 32, 52), batch=self.dialog_batch)

        corners = resource.image("assets/sprites/hud/dialog_corners.png")

        corner0 = sprite.Sprite(corners.get_region(0, 0, 16, 16),
                                x=x, y=y, batch=self.dialog_batch)
        corner1 = sprite.Sprite(corners.get_region(16, 0, 16, 16),
                                x=x + w - 16, y=y, batch=self.dialog_batch)
        corner2 = sprite.Sprite(corners.get_region(0, 16, 16, 16),
                                x=x, y=y + h - 16, batch=self.dialog_batch)
        corner3 = sprite.Sprite(corners.get_region(16, 16, 16, 16),
                                x=x + w - 16, y=y + h - 16, batch=self.dialog_batch)

        close_btn_batch = graphics.Batch()
        pressed = resource.image("assets/sprites/item/1.png")
        unpressed = resource.image("assets/sprites/hud/close.bmp")
        close_btn = gui.PushButton(x=x + w - 16, y=y + h - 16,
                                   pressed=pressed, unpressed=unpressed,
                                   batch=close_btn_batch)
        self.window.push_handlers(close_btn)


        def on_press(_) -> None:
            self.close_dialog(player)

        close_btn.set_handler('on_press', on_press)

        self.dialog_components.extend([
            border0, border1, border2, border3, corner0, corner1, corner2,
            corner3, widnow, close_btn_batch
        ])

        self.active_gui_components.extend(self.dialog_components)
        self.active_gui_components.extend(self.dialog_contents)
        
    def get_dialog_batch(self):
        return self.dialog_batch, self.dialog_components

    def close_dialog(self,player) -> None:
        log("Closing dialog")
        try:
            for component in self.dialog_components:
                try:
                    self.active_gui_components.remove(component)
                except ValueError:
                    warn("Component not found in active GUI components")
        except TypeError:
            warn("No dialog components to remove")
    
        try:
            for component in self.dialog_contents:
                try:
                    self.active_gui_components.remove(component)
                except ValueError:
                    warn("Component not found in active GUI components")
        except TypeError:
            warn("No dialog components to remove")

        self.dialog_components.clear()
        player.can_move = True
        self.dialog = None

