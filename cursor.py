from pyglet.window import ImageMouseCursor
from pyglet import resource

CURSORS = resource.image('assets/sprites/cursor.png')

CROSSHAIR = CURSORS.get_region(16, 16, 16, 16)
POINTER = CURSORS.get_region(0, 16, 16, 16)
HAND = CURSORS.get_region(0, 0, 16, 16)

def set_cursor(window, cursor) -> None:
    window.set_mouse_cursor(ImageMouseCursor(cursor))

