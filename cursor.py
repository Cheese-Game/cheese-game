from pyglet.window import ImageMouseCursor
from pyglet import resource

class Cursor_Class:
    CURSORS = resource.image('assets/sprites/cursor.png')
    scale=16
    crosshairimg=CURSORS.get_region(16, 16, 16, 16)
    #crosshairimg.height=300
    #crosshairimg.width=300
    pointerimg=CURSORS.get_region(0, 16, 16, 16)
    handimg=CURSORS.get_region(0, 0, 16, 16)
    CROSSHAIR = ImageMouseCursor(crosshairimg, hot_x=8, hot_y=8,)
    POINTER = ImageMouseCursor(pointerimg, hot_x=7, hot_y=16)
    HAND = ImageMouseCursor(handimg, hot_x=8, hot_y=8)
    def __init__(self,placholder):
        pass
    def set_cursor(self,window, cursor) -> None:
        window.set_mouse_cursor(cursor)
    def change_size(self,z,window) -> None:
        #the idea is that the size of the cursor should be adjusted
        self.scale=self.scale*z
        self.crosshairimg.width=self.scale
        self.crosshairimg.height=self.scale
        self.pointerimg.width=self.scale
        self.pointerimg.height=self.scale
        self.handimg.width=self.scale
        self.handimg.height=self.scale
        CROSSHAIR = ImageMouseCursor(self.crosshairimg, hot_x=8, hot_y=8,)    
        POINTER = ImageMouseCursor(self.pointerimg, hot_x=7, hot_y=16)
        HAND = ImageMouseCursor(self.handimg, hot_x=8, hot_y=8)
        print("size changed")
        print(self.scale)
        


