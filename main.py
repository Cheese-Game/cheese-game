import pyglet
from player import Player
from tiles import Tileset, Tilemap
from logger import log


class Game:
    WIDTH = 640
    HEIGHT = 480
    SIZE = WIDTH, HEIGHT

    def __init__(self):
        pyglet.app.run()


window = pyglet.window.Window(Game.WIDTH, Game.HEIGHT)


@window.event
def on_draw():
    window.clear()

    for symbol in held_movement_keys:
        match symbol:
            case pyglet.window.key.W:
                player.move(0, player.SPEED)
            case pyglet.window.key.S:
                player.move(0, -player.SPEED)
            case pyglet.window.key.D:
                player.move(player.SPEED, 0)
            case pyglet.window.key.A:
                player.move(-player.SPEED, 0)
    
    tilemap.adjust_position(player.get_pos())

    tilemap.draw()
    player.draw()


@window.event
def on_key_press(symbol, _):
    if symbol in [pyglet.window.key.W, pyglet.window.key.A, pyglet.window.key.S, pyglet.window.key.D]:
        held_movement_keys.append(symbol)
        return

    if symbol == pyglet.window.key.PERIOD:
        tileset.update_tileset('assets/tileset/kitchen.png')
        tilemap.update_tilemap(tileset, 'assets/tilemap/kitchen.json', Game.SIZE)
        player.reset_pos()


@window.event
def on_key_release(symbol, _):
    if symbol in [pyglet.window.key.W, pyglet.window.key.A, pyglet.window.key.S, pyglet.window.key.D]:
        held_movement_keys.remove(symbol)
        return

if __name__ == '__main__':
    player = Player('assets/sprites/player/', Game.SIZE)
    tileset = Tileset('assets/tileset/outside.png')
    tilemap = Tilemap(tileset, 'assets/tilemap/area1.json', Game.SIZE)
    
    held_movement_keys = []
    
    game = Game()
