import pyglet
import pytmx
from player import Player
from new_tilemap import Tilemap
from logger import log
from npc import Child


class Game:
    SIZE = 640, 480
    zoom = 1.0
    
    def __init__(self):
        pyglet.app.run()


window = pyglet.window.Window(*Game.SIZE)
window.view = window.view.scale((Game.zoom, Game.zoom, 1.0))


@window.event
def on_draw():
    #glEnable(GL_BLEND)
    #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    tilemap.adjust_position(player.get_pos())
    # door = tilemap.check_for_door(player.get_pos())

    # if door is not None:
    #     # tileset.update_tileset(f'assets/tileset/{door}.png')
    #     tilemap.update_tilemap(f'assets/tilemap/{door}.json', Game.SIZE)
    #     player.reset_pos()

    window.clear()
    
    # draw order can be modified here

    tilemap.draw()
    player.draw()
    fps_display.draw()
    for child in child_flock:
        child.update(child_flock)


@window.event
def on_key_press(symbol, _):
    if symbol == pyglet.window.key.W:
        pyglet.clock.schedule_interval(player.move_up, 1 / 60.0)
    elif symbol == pyglet.window.key.A:
        pyglet.clock.schedule_interval(player.move_left, 1 / 60.0)
    elif symbol == pyglet.window.key.S:
        pyglet.clock.schedule_interval(player.move_down, 1 / 60.0)
    elif symbol == pyglet.window.key.D:
        pyglet.clock.schedule_interval(player.move_right, 1 / 60.0)

@window.event
def on_key_release(symbol, _):
    if symbol == pyglet.window.key.W:
        pyglet.clock.unschedule(player.move_up)
    elif symbol == pyglet.window.key.A:
        pyglet.clock.unschedule(player.move_left)
    elif symbol == pyglet.window.key.S:
        pyglet.clock.unschedule(player.move_down)
    elif symbol == pyglet.window.key.D:
        pyglet.clock.unschedule(player.move_right)


fps_display = pyglet.window.FPSDisplay(window=window)

pyglet.font.add_file('assets/font/PixelatedElegance.ttf')

label = pyglet.text.Label('Hello, world',
                          font_name='Pixelated Elegance',
                          font_size=36,
                          x=10, y=10)


# tmx_data = pytmx.TiledTileset('assets/tileset/area1/area1.tsx')

# tileset = Tileset('assets/tileset/area1.png')
tilemap = Tilemap('assets/tilemap/area1.tmx', Game.SIZE)

player = Player('assets/sprites/player/', Game.SIZE)

child_flock = []
for i in range(10):
    child_flock.append(Child(0, 0, 1, 1))

held_movement_keys = []

game = Game()
