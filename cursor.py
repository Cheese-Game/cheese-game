from pyglet.window import ImageMouseCursor
from pyglet import resource

CURSORS = resource.image('assets/sprites/cursor.png')

CROSSHAIR = ImageMouseCursor(CURSORS.get_region(16, 16, 16, 16), hot_x=8, hot_y=8)
POINTER = ImageMouseCursor(CURSORS.get_region(0, 16, 16, 16), hot_x=7, hot_y=16)
HAND = ImageMouseCursor(CURSORS.get_region(0, 0, 16, 16), hot_x=8, hot_y=8)

def set_cursor(window, cursor) -> None:
    window.set_mouse_cursor(cursor)

